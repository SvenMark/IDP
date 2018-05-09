from pyax12.connection import Connection
import time

# Connect to the serial port
serial_connection = Connection(port="/dev/ttyAMA0", rpi_gpio=True)

dynamixel_id = 13

# Go to 0°
serial_connection.goto(dynamixel_id, 0, speed=512, degrees=True)
time.sleep(1)    # Wait 1 second

# Go to -45° (45° CW)
serial_connection.goto(dynamixel_id, -45, speed=512, degrees=True)
time.sleep(1)    # Wait 1 second

# Go to -90° (90° CW)
serial_connection.goto(dynamixel_id, -90, speed=512, degrees=True)
time.sleep(1)    # Wait 1 second

# Go to -135° (135° CW)
serial_connection.goto(dynamixel_id, -135, speed=512, degrees=True)
time.sleep(1)    # Wait 1 second

# Go to -150° (150° CW)
serial_connection.goto(dynamixel_id, -150, speed=512, degrees=True)
time.sleep(1)    # Wait 1 second

# Go to +150° (150° CCW)
serial_connection.goto(dynamixel_id, 150, speed=512, degrees=True)
time.sleep(2)    # Wait 2 seconds

# Go to +135° (135° CCW)
serial_connection.goto(dynamixel_id, 135, speed=512, degrees=True)
time.sleep(1)    # Wait 1 second

# Go to +90° (90° CCW)
serial_connection.goto(dynamixel_id, 90, speed=512, degrees=True)
time.sleep(1)    # Wait 1 second

# Go to +45° (45° CCW)
serial_connection.goto(dynamixel_id, 45, speed=512, degrees=True)
time.sleep(1)    # Wait 1 second

# Go back to 0°
serial_connection.goto(dynamixel_id, 0, speed=512, degrees=True)

# Close the serial connection
serial_connection.close()
