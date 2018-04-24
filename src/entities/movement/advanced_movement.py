from entities.movement.movement import Movement


class Advanced(Movement):
    """
    Base class for advanced movements
    """


class Climb(Advanced):
    """
    Should implement methods for climbing
    """
    raise NotImplementedError


class Dance(Advanced):
    """
    Should implement methods for dancing
    """
    raise NotImplementedError
