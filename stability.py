import json
import math
import os

import matplotlib.pyplot as plt

CAPTAIN = "Dev"
SEAWATER_DENSITY = 1.025  # tonnes per cubic metre
SAVE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ships.json")


def calculate_kb(draft):
    return draft / 2


def calculate_bm(beam, draft):
    return (beam ** 2) / (12 * draft)


def calculate_gm(length, beam, draft, kg):
    kb = calculate_kb(draft)
    bm = calculate_bm(beam, draft)
    km = kb + bm
    gm = km - kg
    return gm


def stability_verdict(gm):
    if gm <= 0:
        return f"UNSTABLE - Captain {CAPTAIN}, stop loading! She'll capsize!"
    elif gm < 0.15:
        return f"MARGINAL - careful, Captain {CAPTAIN}. She's dangerously tender."
    else:
        return f"STABLE - smooth sailing, Captain {CAPTAIN}!"


def get_positive_number(prompt):
    while True:
        text = input(prompt)
        try:
            value = float(text)
        except ValueError:
            print("Please enter a number, for example 6.5")
            continue
        if value <= 0:
            print("Value must be greater than zero.")
            continue
        return value


def print_righting_arm_table(gm):
    print("\nHeel (deg) | GZ (m)")
    print("-" * 22)
    for angle in range(0, 41, 10):
        gz = gm * math.sin(math.radians(angle))
        print(f"{angle:>10} | {gz:>6.2f}")


def calculate_loaded_kg(ship_weight, ship_kg, cargo_list):
    total_weight = ship_weight
    total_moment = ship_weight * ship_kg
    for item in cargo_list:
        total_weight += item["weight"]
        total_moment += item["weight"] * item["height"]
    return total_moment / total_weight


def get_cargo():
    cargo_list = []
    while True:
        name = input("Cargo name (or just press Enter to finish): ")
        if name == "":
            break
        weight = get_positive_number("  Weight (tonnes): ")
        height = get_positive_number("  Height above keel (m): ")
        cargo_list.append({"name": name, "weight": weight, "height": height})
    return cargo_list


def plot_gz_curve(gm, ship_name):
    angles = list(range(0, 41, 2))
    gz_values = []
    for angle in angles:
        gz = gm * math.sin(math.radians(angle))
        gz_values.append(gz)

    plt.plot(angles, gz_values, marker="o")
    plt.axhline(0, color="black", linewidth=1)
    plt.title(f"GZ Curve - {ship_name} (GM = {gm:.2f} m)")
    plt.xlabel("Heel angle (degrees)")
    plt.ylabel("GZ righting arm (m)")
    plt.grid(True)
    plt.show()


def calculate_total_weight(ship_weight, cargo_list):
    total = ship_weight
    for item in cargo_list:
        total += item["weight"]
    return total


def calculate_draft(total_weight, length, beam):
    # Archimedes: weight of ship = weight of water it pushes aside
    # total_weight = density * length * beam * draft
    return total_weight / (SEAWATER_DENSITY * length * beam)


def load_ships():
    if not os.path.exists(SAVE_FILE):
        return {}
    try:
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("Warning: ships.json is damaged, starting with an empty fleet.")
        return {}


def save_ships(ships):
    with open(SAVE_FILE, "w") as f:
        json.dump(ships, f, indent=4)


def choose_saved_ship(ships):
    names = list(ships.keys())
    print("Saved ships:")
    for number, name in enumerate(names, start=1):
        print(f"  {number}. {name}")
    choice = input("Type a number to load a ship, or press Enter for a new one: ")
    if choice.isdigit() and 1 <= int(choice) <= len(names):
        return names[int(choice) - 1]
    return None


def ask_new_ship():
    ship_name = input("Name your ship: ") or f"MV {CAPTAIN}"
    ship = {
        "length": get_positive_number("Length (m): "),
        "beam": get_positive_number("Beam (m): "),
        "kg": get_positive_number("Empty ship KG (m): "),
        "weight": get_positive_number("Empty ship weight (tonnes): "),
    }
    return ship_name, ship


def print_banner():
    print("=" * 40)
    print(f"  CAPTAIN {CAPTAIN.upper()}'S STABILITY CALCULATOR")
    print("=" * 40)
    print(r"""
          |\
          | \
       ___|__\___
    ~~~\_________/~~~
    ~~~~~~~~~~~~~~~~~~~
    """)


print_banner()
ships = load_ships()
ship_name = None

if ships:
    ship_name = choose_saved_ship(ships)

if ship_name is not None:
    ship = ships[ship_name]
    print(f"\nLoaded {ship_name} from the fleet.")
else:
    ship_name, ship = ask_new_ship()
    if input("Save this ship for next time? (y/n): ").lower() == "y":
        ships[ship_name] = ship
        save_ships(ships)
        print(f"{ship_name} saved.")

print(f"\nWelcome aboard, Captain {CAPTAIN}. Let's check the {ship_name}.\n")

print("Add cargo:")
cargo = get_cargo()

total_weight = calculate_total_weight(ship["weight"], cargo)
draft = calculate_draft(total_weight, ship["length"], ship["beam"])
loaded_kg = calculate_loaded_kg(ship["weight"], ship["kg"], cargo)
gm = calculate_gm(ship["length"], ship["beam"], draft, loaded_kg)

print(f"\n--- Report for {ship_name} ---")
print(f"Total weight = {total_weight:.0f} tonnes")
print(f"Draft = {draft:.2f} m")
print(f"Loaded KG = {loaded_kg:.2f} m")
print(f"GM = {gm:.2f} m")
print("Verdict:", stability_verdict(gm))
print_righting_arm_table(gm)
plot_gz_curve(gm, ship_name)
print(f"\nFair winds, Captain {CAPTAIN}!")