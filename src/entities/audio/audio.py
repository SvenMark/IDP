import soundfile as sf


class Audio(object):
    @staticmethod
    def getfile(filename):

        return sf.read("../../../resources/" + filename)


