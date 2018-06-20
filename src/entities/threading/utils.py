import sys

sys.path.insert(0, '../../../src')


class SharedObject(object):
    """
    Shared object used in threading to notify threads to stop
    """

    def __init__(self):
        """
        Constructor for Shared Object class
        """
        self.stop = False
        self.has_stopped = True
        self.bluetooth_settings = BluetoothSettings()

    def has_to_stop(self):
        """
        Get status has to stop
        :return: if Thread has to stop
        """
        return self.stop

    # Set status
    def has_been_stopped(self):
        """
        Set status has been stopped to notify the main thread that the current thread
        has stopped
        :return: Thread has stopped
        """
        self.has_stopped = True


class BluetoothSettings(object):
    def __init__(self):
        self.s = 0
        self.v = 0
        self.h = 0
        self.d = 0
        self.x = 0
        self.y = 0
        self.m = 0

    def handle_values(self, s, v, h, d, x, y, m):
        self.s = s
        self.v = v
        self.h = h
        self.d = d
        self.x = x
        self.y = y
        self.m = m





