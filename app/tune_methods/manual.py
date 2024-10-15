from app.systems.system import CloseLoopSystem, System


class Manual(System):
    def __init__(self, controller, pade_order=1) -> None:
        super().__init__(controller, pade_order)

    def tune(
        self, k: float, tau: float, theta: float, overshoot: bool = False, lambda_val: float = None
    ) -> CloseLoopSystem:
        kp = (1.2 * tau) / (k * theta)
        ti = 2 * tau
        td = theta / 2

        t, power, overshoot, rise_time = self.pid_response(k, tau, theta, kp, ti, td)

        return CloseLoopSystem(t, power, overshoot, rise_time, kp, ti, td)

    def manual_tune(self, k: float, tau: float, theta: float, kp: float, ti: float, td: float):
        t, power, overshoot, rise_time = self.pid_response(k, tau, theta, kp, ti, td)

        return CloseLoopSystem(t, power, overshoot, rise_time, kp, ti, td)
