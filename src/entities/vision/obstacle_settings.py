import sys
sys.path.insert(0, '../../../src')


class ObstacleSettings(object):
    def __init__(self):
        # For each frame update
        self.update = False

        # If stairs are still visible
        self.stairs = False

        # If bridge is detected
        self.bridge = False
        self.bridge_position = 50

        # If the cup is detected
        self.cup_detected = False
        self.cup_position = 50
        self.cup_size = 10
