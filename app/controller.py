from numpy import ndarray
from scipy.io import loadmat


class Controller:
    def __init__(self):
        self._dataset: dict | None = None
        self._step: ndarray | None = None
        self._engine_power: ndarray | None = None

    @property
    def dataset(self):
        return self._dataset

    @dataset.setter
    def dataset(self, path: str):
        """Read the dataset and separate into step and engine power

        :param path: Where the dataset is located
        """
        self._dataset = loadmat(path)
        self._step = self._dataset["TARGET_DATA____ProjetoC213_Degrau"]
        self._engine_power = self._dataset["TARGET_DATA____ProjetoC213_PotenciaMotor"]


controller = Controller()
