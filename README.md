# Arduino_ControlWithPS4
A few scripts to control an Arduino robot Arm with a PS4 (DualShock4) controller, or a Keyboard.

## What the scripts do:
- serialMonitor.ino is the code that is uploaded onto the Arduino. The script basically defines which Pins the motors are connected to, and the serial rate.
- ControllerControl.py file uses the Dualshock Controller, along with PyGame, to find the controller inputs, and then pass them through Serial to the Arduino.
- KeyboardControl.py does the exact same as ControllerControl.py
