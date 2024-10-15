import numpy as np


class Evaluation:
    @staticmethod
    def mse(data, model):
        return np.sqrt(np.mean((data - model) ** 2))
