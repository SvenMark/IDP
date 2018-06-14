import platform

#from main import RESOURCES


class Audio(object):
    """
    Base class for all audio implementations
    """
    def __init__(self):
        self.windows = True if "Windows" == platform.system() else False
        self.resources = "../../resources/"

    def get_file_path(self, file_name):
        """
        Gets resource path
        :param file_name: The requested file
        :return: String
        """
        return self.resources + file_name
