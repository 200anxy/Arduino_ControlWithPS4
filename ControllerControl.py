import pygame
import serial
import time

# Initialize Pygame
pygame.init()

# Set up the serial connection
# IMPORTANT: Changed port to COM6
ser = serial.Serial('COM6', 115200, timeout=1)

# Wait for the serial connection to initialize
time.sleep(2)

print("Searching for game controllers...")
try:
    pygame.joystick.init()
    joystick_count = pygame.joystick.get_count()
    if joystick_count == 0:
        print("No controllers found. Please connect your controller.")
        exit()
    else:
        controller = pygame.joystick.Joystick(0)
        controller.init()
        print(f"Controller found: {controller.get_name()}")
        print("Use joysticks and R2/L2 triggers. Press 'X' to exit.")

except pygame.error as e:
    print(f"Error initializing joystick: {e}")
    ser.close()
    exit()

# Set a sensitivity multiplier for faster movement
sensitivity = 2.0  # Adjust this value to change the speed
dead_zone = 0.1  # Set a dead zone to prevent movement when sticks are at rest

def apply_dead_zone(value, dead_zone):
    if abs(value) < dead_zone:
        return 0.0
    else:
        # Scale the value to use the full range outside the dead zone
        if value > 0:
            return (value - dead_zone) / (1 - dead_zone)
        else:
            return (value + dead_zone) / (1 - dead_zone)

# Main loop
try:
    while True:
        # Check for events to update joystick state
        pygame.event.pump()

        # Read analog stick values (ranges from -1.0 to 1.0)
        right_x = controller.get_axis(2) # Right stick, X-axis
        right_y = controller.get_axis(3) # Right stick, Y-axis
        left_x = controller.get_axis(0)  # Left stick, X-axis
        left_y = controller.get_axis(1)  # Left stick, Y-axis
        
        # Read R2 and L2 triggers
        # L2 is typically axis 4 and R2 is axis 5 on a PS4 controller
        l2_trigger = controller.get_axis(4) 
        r2_trigger = controller.get_axis(5)

        # Check for the 'X' button to exit
        if controller.get_button(0): # 'X' button is index 0
            print("Exiting...")
            ser.close()
            pygame.quit()
            exit()

        # Apply dead zone to joystick values
        right_x = apply_dead_zone(right_x, dead_zone)
        right_y = apply_dead_zone(right_y, dead_zone)
        left_x = apply_dead_zone(left_x, dead_zone)
        left_y = apply_dead_zone(left_y, dead_zone)

        # Map analog values to a more responsive range
        servo_speeds = [0.0] * 5
        servo_speeds[4] = -right_x * sensitivity  # Base (D6)
        servo_speeds[3] = -right_y * sensitivity  # Arm (D5)
        servo_speeds[1] = left_x * sensitivity    # Wrist (D3)
        servo_speeds[2] = left_y * sensitivity    # Elbow (D4)

        # Map R2/L2 to the Pincer (D2)
        pincer_speed = 0.0
        if r2_trigger > -0.5:  # Check if R2 is being pressed
            pincer_speed = (r2_trigger + 1) / 2 # Scale to 0-1 range
            servo_speeds[0] = pincer_speed * sensitivity # Open
        elif l2_trigger > -0.5: # Check if L2 is being pressed
            pincer_speed = (l2_trigger + 1) / 2 # Scale to 0-1 range
            servo_speeds[0] = -pincer_speed * sensitivity # Close
        else:
            servo_speeds[0] = 0.0
        
        # Send the values to the Arduino
        data_to_send = ','.join([f"{s:.2f}" for s in servo_speeds]) + '\n'
        ser.write(data_to_send.encode())
        
        # A short delay to prevent flooding the serial port
        time.sleep(0.005)

except Exception as e:
    print(f"An error occurred: {e}")
    ser.close()
    pygame.quit()
    exit()