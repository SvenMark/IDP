import sys
sys.path.insert(0, '../../../src')


class RecognizeSettings(object):
    def __init__(self, grab_distance=183,
                 recognize_distance_max=250,
                 recognize_distance_min=130):

        # If the black tape from start position has been detected, robot should stop if this is true
        self.black_detected = False

        # The last known position of the building on the screen
        self.current_position = 50

        # Tells how the building should be grabbed, depending which side is in front of the robot
        self.pick_up_vertical = False

        # If the robot should try to grab, robot is close enough
        self.grab = False

        # If There has been detected a new building
        self.new = False

        # (estimated) distance between camera and building
        # only important if new building detected and grabbing has failed
        #  to determine where the robot should move to for a new grabbing attempt
        self.distance = -1

        # If this settings had been updated, not been handled yet by movement thread
        # Vision thread sets it to true after each handled frame and the movement thread sets it to false when handled
        self.update = False

        # Maximum distance where the robot should attempt to grab the building
        self.grab_distance = grab_distance

        # Distances where the vision thread should start recognize the building
        self.recognize_distance_max = recognize_distance_max
        self.recognize_distance_min = recognize_distance_min

