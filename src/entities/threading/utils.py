import sys

sys.path.insert(0, '../../../src')


class SharedObject(object):
    """

    """

    def __init__(self):
        """

        """
        self.stop = False
        self.has_stopped = True

    # Get status
    def has_to_stop(self):
        """

        :return:
        """
        return self.stop

    # Set status
    def has_been_stopped(self):
        """

        :return:
        """
        self.has_stopped = True

