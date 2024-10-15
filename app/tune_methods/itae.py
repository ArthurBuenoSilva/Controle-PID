from app.systems.system import CloseLoopSystem, System


class ITAE(System):
    def __init__(self, controller, pade_order=1) -> None:
        super().__init__(controller, pade_order)

    def tune(
        self, k: float, tau: float, theta: float, overshoot: bool = False, lambda_val: float = None
    ) -> CloseLoopSystem:
        kp = (0.965 / k) * (tau / theta) ** (-0.85)
        ti = tau / (0.796 + (-0.147 * (theta / tau)))
        td = tau * 0.308 * (theta / tau) ** 0.929

        t, power, overshoot, rise_time = self.pid_response(k, tau, theta, kp, ti, td)

        return CloseLoopSystem(t, power, overshoot, rise_time, kp, ti, td)
