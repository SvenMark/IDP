class Audio(object):
    """
    Base class for audio
    """
    raise NotImplementedError


class Speak(Audio):
    """
    Should implement methods for music output
    """
    raise NotImplementedError


class Listen(Audio):
    """
    Should implement methods for music input
    """
    raise NotImplementedError
