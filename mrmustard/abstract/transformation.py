import numpy as np  # for repr
from abc import ABC
from mrmustard import GaussianPlugin
from mrmustard.abstract import State
from mrmustard._typing import *

class Transformation(ABC):
    r"""
    Base class for all transformations.
    Transformations include:
        * unitary transformations
        * non-unitary CPTP channels
    Given that measurements are CP but not TP, they have their own abstract class.
    """

    _gaussian = GaussianPlugin()

    def __call__(self, state: State) -> State:
        d = self.d_vector(state.hbar)
        X = self.X_matrix(state.hbar)
        Y = self.Y_matrix(state.hbar)

        output = State(state.num_modes, hbar=state.hbar, mixed=Y is not None)
        output.cov, output.means = self._gaussian.CPTP(state.cov, state.means, X, Y, d, self._modes)
        return output

    def __repr__(self):
        with np.printoptions(precision=6, suppress=True):
            lst = [f"{name}={np.array(np.atleast_1d(self.__dict__[name]))}" for name in self.param_names]
            return f"{self.__class__.__qualname__}(modes={self._modes}, {', '.join(lst)})"

    def X_matrix(self, hbar: float) -> Optional[Matrix]:
        return None

    def d_vector(self, hbar: float) -> Optional[Vector]:
        return None

    def Y_matrix(self, hbar: float) -> Optional[Matrix]:
        return None

    def trainable_parameters(self) -> Dict[str, List[Trainable]]:
        return {
            "symplectic": [],
            "orthogonal": [],
            "euclidean": self._trainable_parameters}
