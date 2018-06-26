import sys
sys.path.insert(0, '../../../src')


class ObstacleSettings(object):
    def __init__(self):
        # Als je een frame verwerkt hebt
        self.update = False

        # Als je de beker hebt gedetecteerd
        self.cup_detected = False

        # Positie van de beker
        self.cup_position = 50
