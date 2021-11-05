# this is the topmost __init__.py file of the mrmustard package

import importlib
from rich.pretty import install

install()  # NOTE: just for the looks, not stricly required

__version__ = "0.1.0"


class Settings:
    def __init__(self):
        self._backend = "tensorflow"
        self.HBAR = 2.0
        self.TMSV_DEFAULT_R = 3.0

    @property
    def backend(self):
        return self._backend

    # property setter for backend
    @backend.setter
    def backend(self, backend_name: str):
        if backend_name not in ["tensorflow", "pytorch"]:
            raise ValueError("Backend must be either 'tensorflow' or 'pytorch'")
        self._backend = backend_name
        self.__activate_backend()

    def __activate_backend(self):
        "Activates the math backend in the modules where it is used"
        from mrmustard.physics import fock, gaussian
        from mrmustard.utils import training, xptensor

        math = importlib.import_module(f"mrmustard.math.{self.backend}").Math()
        vars(fock)["math"] = math
        vars(gaussian)["math"] = math
        vars(training)["math"] = math
        vars(xptensor)["math"] = math


settings = Settings()
settings.backend = "tensorflow"
