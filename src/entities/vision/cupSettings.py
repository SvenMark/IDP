import sys

sys.path.insert(0, '../../../src')


class CupSettings(object):
    def __init__(self):
        # Als je een frame verwerkt hebt
        self.update = False

        # als je de beker hebt gedetecteerd
        self.cup_detected = False

        # positie van de beker
        self.cup_position = 50
