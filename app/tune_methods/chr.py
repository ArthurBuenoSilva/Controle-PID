from app.systems.system import CloseLoopSystem, System


class CHR(System):
    def __init__(self, controller, pade_order=1) -> None:
        super().__init__(controller, pade_order)

    def tune(
        self, k: float, tau: float, theta: float, overshoot: bool = False, lambda_val: float = None
    ) -> CloseLoopSystem:
        if overshoot:
            kp = (0.95 * tau) / (k * theta)
            ti = 1.357 * tau
            td = 0.473 * theta
        else:
            kp = (0.6 * tau) / (k * theta)
            ti = tau
            td = theta / 2

        t, power, overshoot, rise_time = self.pid_response(k, tau, theta, kp, ti, td)

        return CloseLoopSystem(t, power, overshoot, rise_time, kp, ti, td)
