import sys

sys.path.insert(0, '../../../src')

from entities.threading.BluetoothSettings import BluetoothSettings


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





