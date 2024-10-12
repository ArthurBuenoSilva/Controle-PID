import numpy as np


class SysIdentification:
    @staticmethod
    def smith_method(time, power, step):
        power_normalized = SysIdentification.normalize(power)
        final_value = power_normalized[-1]
        k = final_value / np.mean(step)

        t1 = time[np.where(power_normalized >= 0.283 * final_value)[0][0]]
        t2 = time[np.where(power_normalized >= 0.632 * final_value)[0][0]]

        tau = 1.5 * (t2 - t1)
        theta = t2 - tau
        return k, tau, theta

    @staticmethod
    def sundaresan_method(time, power, step):
        power_normalized = SysIdentification.normalize(power)
        final_value = power_normalized[-1]
        k = final_value / np.mean(step)

        t1 = time[np.where(power_normalized >= 0.353 * final_value)[0][0]]
        t2 = time[np.where(power_normalized >= 0.853 * final_value)[0][0]]

        tau = (2 / 3) * (t2 - t1)
        theta = (1.3 * t1) - (0.29 * t2)
        return k, tau, theta

    @staticmethod
    def normalize(data):
        return data - data[0]
