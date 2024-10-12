from app.systems.system import CloseLoopSystem, System


class CohenCoon(System):
    def __init__(self, controller, pade_order=1) -> None:
        super().__init__(controller, pade_order)

    def tune(
        self, k: float, tau: float, theta: float, overshoot: bool = False, lambda_val: float = None
    ) -> CloseLoopSystem:
        kp = (tau / (k * theta)) * ((16 * tau + 3 * theta) / (12 * tau))
        ti = theta * ((32 + (6 * theta) / tau) / (13 + (8 * theta) / tau))
        td = (4 * theta) / (11 + (2 * theta) / tau)

        t, power, overshoot, rise_time = self.pid_response(k, tau, theta, kp, ti, td)

        return CloseLoopSystem(t, power, overshoot, rise_time, kp, ti, td)
