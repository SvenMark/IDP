
class SharedObject(object):

    def __init__(self):
        self.stop = False
        self.has_stopped = False

    # Get status
    def has_to_stop(self):
        return self.stop

    # Set status
    def has_been_stopped(self):
        self.has_stopped = True

