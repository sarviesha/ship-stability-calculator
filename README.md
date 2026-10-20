# Captain Dev's Ship Stability Calculator

A beginner Python project that estimates the stability of a simple
box-shaped ship (a rectangular barge): GM, righting arm table, GZ graph,
cargo loading, and saved ship profiles.

## How to run

1. Install Python 3 from python.org (tick "Add Python to PATH" on Windows).
2. Open a terminal in this folder and install the graph library:

       python -m pip install -r requirements.txt

3. Run the program:

       python stability.py

Saved ships are stored in `ships.json`, which the program creates itself.

## Limits

This is a learning tool using simplified formulas (box-shaped hull, small-angle
GZ). It is NOT for real loading or navigation decisions.
