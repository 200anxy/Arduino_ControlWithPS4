import serial
import keyboard
import time

# Set up the serial connection
# IMPORTANT: Change 'COM6' to the correct port for your Arduino
ser = serial.Serial('COM6', 115200, timeout=1)

# Wait for the serial connection to initialize
time.sleep(2)

print("Robot Arm Control Ready. Press WASD, RF, TG, QE. Press 'X' to exit.")

# Define the speed for each motor
speed = 1.0

# Main loop to check for key presses
try:
    while True:
        # Array to hold the speed for each servo
        servo_speeds = [0.0] * 5

        # Check for each key and set the corresponding servo speed
        if keyboard.is_pressed('w'):
            servo_speeds[4] = speed  # Base (D6)
        elif keyboard.is_pressed('s'):
            servo_speeds[4] = -speed

        if keyboard.is_pressed('a'):
            servo_speeds[1] = speed  # Wrist (D3)
        elif keyboard.is_pressed('d'):
            servo_speeds[1] = -speed
            
        if keyboard.is_pressed('r'):
            servo_speeds[2] = speed # Elbow (D4)
        elif keyboard.is_pressed('f'):
            servo_speeds[2] = -speed

        if keyboard.is_pressed('t'):
            servo_speeds[3] = speed # Arm (D5)
        elif keyboard.is_pressed('g'):
            servo_speeds[3] = -speed

        if keyboard.is_pressed('q'):
            servo_speeds[0] = speed # Pincer (D2)
        elif keyboard.is_pressed('e'):
            servo_speeds[0] = -speed
        
        # Check for 'x' to exit
        if keyboard.is_pressed('x'):
            print("Exiting...")
            break

        # Send the values to the Arduino
        data_to_send = ','.join([f"{s:.2f}" for s in servo_speeds]) + '\n'
        ser.write(data_to_send.encode())
        
        # A short delay to prevent flooding the serial port
        time.sleep(0.01)

except Exception as e:
    print(f"An error occurred: {e}")
    
finally:
    ser.close()
    print("Serial port closed.")