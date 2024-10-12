from app.systems.system import CloseLoopSystem, System

"""
λ/θ should be greater than 0.8. For many systems, an ideal ratio is between 1 and 2:

λ/θ≈1: A good balance between performance and robustness.

λ/θ≈1.5: Provides greater robustness, useful in systems with noise or uncertainties in the model.

λ/θ≥2: Even greater robustness, with slower responses. This can be used for processes that are more sensitive to variations in the model or to minimize overshoot.
Typical values depending on the process
Systems with low noise and low uncertainty in the model

λ/θ close to 1 (faster response).

Systems with more noise or greater uncertainty:

λ/θ between 1.5 and 2 (more robust).

Higher lambda, greater accuracy but longer response time
"""


class IMC(System):
    def __init__(self, controller, pade_order=1) -> None:
        super().__init__(controller, pade_order)

    def tune(
        self, k: float, tau: float, theta: float, overshoot: bool = False, lambda_val: float = None
    ) -> CloseLoopSystem:
        # IMC vars
        kp = (2 * tau + theta) / (k * (2 * lambda_val + theta))
        ti = (theta / 2) + tau
        td = (tau * theta) / (2 * tau + theta)

        t, power, overshoot, rise_time = self.pid_response(k, tau, theta, kp, ti, td)

        return CloseLoopSystem(t, power, overshoot, rise_time, kp, ti, td)
