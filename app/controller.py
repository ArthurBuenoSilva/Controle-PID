from numpy import ndarray
from scipy.io import loadmat

from app import socketio
from app.systems.sys_identification import SysIdentification
from app.systems.system import System
from app.tune_methods.chr import CHR
from app.tune_methods.cohen_coon import CohenCoon
from app.tune_methods.imc import IMC
from app.tune_methods.itae import ITAE
from app.tune_methods.ziegler_nichols import ZieglerNichols


class Controller:
    def __init__(self):
        self._dataset: dict | None = None
        self._step: ndarray | None = None
        self._time: ndarray | None = None
        self._engine_power: ndarray | None = None
        self._tune_methods: dict[str, System] = {
            "CHR": CHR(self),
            "Cohen and Coon": CohenCoon(self),
            "IMC": IMC(self),
            "ITAE": ITAE(self),
            "Ziegler and Nichols": ZieglerNichols(self),
        }
        self._k: float = 0
        self._tau: float = 0
        self._theta: float = 0

    @property
    def dataset(self):
        return self._dataset

    @dataset.setter
    def dataset(self, path: str):
        """Read the dataset and separate into step and engine power

        :param path: Where the dataset is located
        """
        self._dataset = loadmat(path)
        self.step = self._dataset
        self.time = self._dataset
        self.engine_power = self._dataset

    @property
    def step(self):
        return self._step

    @step.setter
    def step(self, dataset: dict):
        self._step = dataset["TARGET_DATA____ProjetoC213_Degrau"][:, 1]

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, dataset: dict):
        self._time = dataset["TARGET_DATA____ProjetoC213_Degrau"][:, 0]

    @property
    def engine_power(self):
        return self._engine_power

    @engine_power.setter
    def engine_power(self, dataset: dict):
        self._engine_power = dataset["TARGET_DATA____ProjetoC213_PotenciaMotor"][:, 1]

    @property
    def tune_methods(self):
        return self._tune_methods

    def identification_method(self):
        """System identification using Smith and Sundaresan methods

        :return: Data to plot charts
        """
        system = System(self, 20)

        # Smith
        k, tau, theta = SysIdentification.smith_method(self.time, self.engine_power, self.step)
        smith_open_loop, smith_close_loop = system.system_response(k, tau, theta)

        self._k = k
        self._tau = tau
        self._theta = theta

        # Sundaresan
        k, tau, theta = SysIdentification.sundaresan_method(self.time, self.engine_power, self.step)
        sundaresan_open_loop, sundaresan_close_loop = system.system_response(k, tau, theta)

        socketio.emit(
            "plotIdentificationMethod",
            {
                "smith": {
                    "openLoop": {
                        "time": smith_open_loop.t.tolist(),
                        "response": smith_open_loop.p.tolist(),
                    },
                    "closeLoop": {
                        "time": sundaresan_close_loop.t.tolist(),
                        "response": sundaresan_close_loop.p.tolist(),
                    },
                },
                "sundaresan": {
                    "openLoop": {
                        "time": sundaresan_open_loop.t.tolist(),
                        "response": sundaresan_open_loop.p.tolist(),
                    },
                    "closeLoop": {
                        "time": sundaresan_close_loop.t.tolist(),
                        "response": sundaresan_close_loop.p.tolist(),
                    },
                },
                "power": self._engine_power.tolist(),
            },
        )

        socketio.emit(
            "chosenMethod",
            {"method": "Smith", "k": round(self._k, 4), "tau": round(self._tau, 4), "theta": round(self._theta, 4)},
        )

    def pid_tune(self, method: str = "", overshoot: bool = False, lambda_val: float = None):
        if method:
            tune_method = self._tune_methods[method]
            pid = tune_method.tune(self._k, self._tau, self._theta, overshoot, lambda_val)

            socketio.emit(
                "tune",
                {
                    "method": method,
                    "time": pid.t.tolist(),
                    "response": pid.p.tolist(),
                    "overshoot": round(pid.overshoot, 4),
                    "rise_time": round(pid.rise_time, 4),
                    "kp": round(pid.kp, 4),
                    "ti": round(pid.ti, 4),
                    "td": round(pid.td, 4),
                },
            )

            return

        socketio.emit("notify", {"message": "Opção inválida", "category": "warning"})


controller = Controller()
