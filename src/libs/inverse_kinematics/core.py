"""Core features."""

from numbers import Number

import autograd.numpy as np

from .component import Link, Joint
from .solver import FKSolver, IKSolver
from .optimizer import ScipyOptimizer


class TinyActuator(object):
    """Represents an actuator as a set of links and revolute joints."""

    def __init__(self, tokens, optimizer=ScipyOptimizer(), max_angles=None, min_angles=None):
        """Create an actuator from specified link lengths and joint axes."""
        components = []
        for t in tokens:
            if isinstance(t, Number):
                components.append(Link([t, 0., 0.]))
            elif isinstance(t, list) or isinstance(t, np.ndarray):
                components.append(Link(t))
            elif isinstance(t, str) and t in {'x', 'y', 'z'}:
                components.append(Joint(t))
            else:
                raise ValueError(
                    'the arguments need to be '
                    'link length or joint axis: {}'.format(t)
                )

        servo_num = len(
            [c for c in components if isinstance(c, Joint)]
        )

        if (max_angles is not None and servo_num != len(max_angles)):
            raise ValueError('Number of angles does not match number of max_angles')
        if (min_angles is not None and servo_num != len(min_angles)):
            raise ValueError('Number of angles does not match number of min_angles')

        self._fk = FKSolver(components)
        self._ik = IKSolver(self._fk, optimizer, max_angles=max_angles, min_angles=min_angles)

        self.angles = [0.] * servo_num

    @property
    def angles(self):
        """The joint angles."""
        return self._angles

    @angles.setter
    def angles(self, angles):
        self._angles = np.array(angles)

    @property
    def ee(self):
        """The end-effector position."""
        return self._fk.solve(self.angles)

    @ee.setter
    def ee(self, position):
        # self.angles = self._ik.solve(self.angles, position)
        self.angles = self._ik.solve([0,0,0], position)
