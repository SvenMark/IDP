class Tracks(object):
    def __init__(self, tracks):
        self.tracks = tracks

    @property
    def get_tracks_count(self):
        return len(self.tracks)

    def forward(self):
        for track in self.tracks:
            track.forward(1, 0)

    def backward(self):
        for track in self.tracks:
            track.backward(1, 0)

    def turn_right(self, duty_cycle_track_right, duty_cycle_track_left, delay):
        self.tracks[0].backward(duty_cycle_track_right, 0)

        self.tracks[1].forward(duty_cycle_track_left, delay)

    def turn_left(self, duty_cycle_track_right, duty_cycle_track_left, delay):
        self.tracks[1].forward(duty_cycle_track_right, 0)

        self.tracks[0].backward(duty_cycle_track_left, delay)
