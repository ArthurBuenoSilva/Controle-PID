from numpy import ndarray
from scipy.io import loadmat

from app import socketio
from app.systems.sys_identification import SysIdentification
from app.systems.system import System
from app.tune_methods.chr import CHR
from app.tune_methods.cohen_coon import CohenCoon
from app.tune_methods.imc import IMC
from app.tune_methods.itae import ITAE
from app.tune_methods.manual import Manual
from app.tune_methods.ziegler_nichols import ZieglerNichols
from app.utils.evaluation import Evaluation


class Controller:
    def __init__(self):
        self._dataset: dict | None = None
        self._step: ndarray | None = None
        self._time: ndarray | None = None
        self._engine_power: ndarray | None = None
        self._tune_methods: dict[str, System] = {
            "CHR": CHR(self, 20),
            "Cohen and Coon": CohenCoon(self, 20),
            "IMC": IMC(self, 20),
            "ITAE": ITAE(self, 20),
            "Ziegler and Nichols": ZieglerNichols(self, 20),
            "Manual": Manual(self, 20),
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

    def get_identification_method_result(self, method: str):
        if method == "smith":
            k, tau, theta = SysIdentification.smith_method(self.time, self.engine_power, self.step)
        else:
            k, tau, theta = SysIdentification.sundaresan_method(self.time, self.engine_power, self.step)

        return k, tau, theta

    def identification_method(self, method: str):
        """System identification using Smith and Sundaresan methods

        :return: Data to plot charts
        """
        try:
            system = System(self, 20)

            # Smith
            k, tau, theta = SysIdentification.smith_method(self.time, self.engine_power, self.step)
            smith_close_loop, smith_open_loop = system.system_response(k, tau, theta)
            smith_ol_mse = Evaluation.mse(smith_open_loop.p, self._engine_power)
            smith_cl_mse = Evaluation.mse(smith_close_loop.p, self._engine_power)

            # Sundaresan
            k, tau, theta = SysIdentification.sundaresan_method(self.time, self.engine_power, self.step)
            sundaresan_close_loop, sundaresan_open_loop = system.system_response(k, tau, theta)
            sundaresan_ol_mse = Evaluation.mse(sundaresan_open_loop.p, self._engine_power)
            sundaresan_cl_mse = Evaluation.mse(sundaresan_close_loop.p, self._engine_power)

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

            k, tau, theta = self.get_identification_method_result(method)

            self._k = k
            self._tau = tau
            self._theta = theta

            socketio.emit(
                "chosenMethod",
                {
                    "k": round(k, 3),
                    "tau": round(tau, 3),
                    "theta": round(theta, 3),
                    "smith_ol_mse": round(smith_ol_mse, 3),
                    "smith_cl_mse": "∞" if smith_cl_mse > 10 ^ 10 else round(smith_cl_mse, 3),
                    "sundaresan_ol_mse": round(sundaresan_ol_mse, 3),
                    "sundaresan_cl_mse": "∞" if sundaresan_cl_mse > 10 ^ 10 else round(sundaresan_cl_mse, 3),
                },
            )
        except Exception as e:
            socketio.emit("notify", {"message": f"Erro inesperado - {e}", "category": "error"})

    def pid_tune(
        self,
        identification: str = "",
        method: str = "",
        pade: int = 20,
        overshoot: bool = False,
        lambda_val: float = None,
    ):
        try:
            if method:
                tune_method = self._tune_methods[method]
                k, tau, theta = self.get_identification_method_result(identification)
                tune_method.pade_order = pade
                pid = tune_method.tune(k, tau, theta, overshoot, lambda_val)

                socketio.emit(
                    "tune",
                    {
                        "method": method,
                        "time": pid.t.tolist(),
                        "response": pid.p.tolist(),
                        "overshoot": round(pid.overshoot, 3),
                        "rise_time": round(pid.rise_time, 3) if pid.rise_time is not None else "-",
                        "k": round(k, 3),
                        "tau": round(tau, 3),
                        "theta": round(theta, 3),
                        "kp": round(pid.kp, 3),
                        "ti": round(pid.ti, 3),
                        "td": round(pid.td, 3),
                    },
                )

                return

            socketio.emit("notify", {"message": "Opção inválida", "category": "warning"})
        except Exception as e:
            socketio.emit("notify", {"message": f"Erro inesperado - {e}", "category": "error"})

    def manual_pid_tune(self, identification: str, pade: int, kp: float, ti: float, td: float):
        try:
            k, tau, theta = self.get_identification_method_result(identification)
            pid = Manual(self, pade).manual_tune(k, tau, theta, kp, ti, td)

            socketio.emit(
                "tune",
                {
                    "method": "Manual",
                    "time": pid.t.tolist(),
                    "response": pid.p.tolist(),
                    "overshoot": round(pid.overshoot, 3),
                    "rise_time": round(pid.rise_time, 3) if pid.rise_time is not None else "-",
                    "k": round(k, 3),
                    "tau": round(tau, 3),
                    "theta": round(theta, 3),
                    "kp": round(pid.kp, 3),
                    "ti": round(pid.ti, 3),
                    "td": round(pid.td, 3),
                },
            )
        except Exception as e:
            socketio.emit("notify", {"message": f"Erro inesperado - {e}", "category": "error"})


controller = Controller()
