from typing import Any

import control
import numpy as np
from control import TransferFunction
from control.matlab import pade

from app.systems.loop_sys import CloseLoopSystem, OpenLoopSystem


class System:
    def __init__(self, controller, pade_order: int = 1) -> None:
        self.controller = controller
        self.pade_order = pade_order

    def tune(
        self, k: float, tau: float, theta: float, overshoot: bool = False, lambda_val: float = None
    ) -> CloseLoopSystem:
        pass

    def open_loop_with_delay(self, k: float, tau: float, theta: float) -> TransferFunction:
        num_pade, den_pade = pade(theta, self.pade_order)

        sys = control.tf([k], [tau, 1])  # First-order system without delay
        sys_pade = control.tf(num_pade, den_pade)  # Delay approximation using Pade
        open_loop = control.series(sys, sys_pade)

        return open_loop

    def close_loop_with_delay(self, k: float, tau: float, theta: float) -> TransferFunction:
        sys = self.open_loop_with_delay(k, tau, theta)
        close_loop = control.feedback(sys)

        return close_loop

    def system_response(self, k: float, tau: float, theta: float):
        sys = self.open_loop_with_delay(k, tau, theta)
        close_loop = control.feedback(sys)

        t_open, power_open = self.step_response(sys)
        t_closed, power_closed = self.step_response(close_loop)

        return CloseLoopSystem(t_closed, power_closed), OpenLoopSystem(t_open, power_open)

    def step_response(self, sys: control.TransferFunction) -> Any:
        t, power = control.step_response(sys * np.mean(self.controller.step), T=self.controller.time)

        return t, power

    @staticmethod
    def rise_time(t: np.ndarray, response: np.ndarray):
        final_value = response[-1]

        # Time to go from 10% to 90% of final value
        rise_time_start = final_value * 0.1
        rise_time_end = final_value * 0.9
        rise_time_indices = np.where((response >= rise_time_start) & (response <= rise_time_end))[0]

        if len(rise_time_indices) > 0:
            t_rise_start = t[rise_time_indices[0]]
            t_rise_end = t[rise_time_indices[-1]]
            rise_time = t_rise_end - t_rise_start
        else:
            rise_time = None

        return rise_time

    @staticmethod
    def overshoot(response: np.ndarray) -> float:
        final_value = response[-1]

        peak_value = np.max(response)
        overshoot = ((peak_value - final_value) / final_value) * 100

        return overshoot

    def pid_response(self, k: float, tau: float, theta: float, kp: float, ti: float, td: float):
        ki = kp / ti
        kd = kp * td
        pid = control.tf([kd, kp, ki], [1, 0])

        open_loop = self.open_loop_with_delay(k, tau, theta)
        cs = control.series(open_loop, pid)

        close_loop = control.feedback(cs)
        t, power = self.step_response(close_loop)
        overshoot = self.overshoot(power)
        rise_time = self.rise_time(t, power)

        return t, power, overshoot, rise_time
