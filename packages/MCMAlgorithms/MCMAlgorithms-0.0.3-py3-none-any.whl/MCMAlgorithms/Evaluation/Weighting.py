import numpy as np


class AHP:

    def __init__(self):
        self.__RI = [0, 0, 0.52, 0.89, 1.12, 1.26, 1.36, 1.41, 1.46, 1.49, 1.52, 1.54, 1.56, 1.58, 1.59, 1.5943,
                     1.6064, 1.6133, 1.6207, 1.6292, 1.6385, 1.6403, 1.6462, 1.6497, 1.6556, 1.6587, 1.6631,
                     1.667]

    def weighting(self, importance_mtx):
        """
        Apply AHP for weight calculation
        :param importance_mtx: square ndarray or torch tensor, AHP importance matrix
        :return: 1-D ndarray, weight of each factor. For situation where importance matrix does not pass the
                 consistency inspection, return a vector fill with -1.
        """
        # Eigvalue
        eig_vals, eig_vecs = np.linalg.eig(importance_mtx)
        max_idx = np.argmax(eig_vals)
        # Consistency Inspection
        max_eig = eig_vals[max_idx]
        n = importance_mtx.shape[0]
        CI = (max_eig - n) / (n - 1)
        RI = self.__RI[n - 1]
        CR = CI / RI
        # Ensure weighting
        weight = np.abs(np.real(eig_vecs[:, max_idx].squeeze()) if CR < 0.1 else -1 * np.ones(n))
        weight /= np.sum(weight)
        return weight


class Entropy:

    def weighting(self, data):
        """
        Apply Entropy weighting for weight calculation
        :param data: 2-D ndarray of data matrix, with each row as a sample
        :return: 1-D ndarray, weight of each factor
        """
        # Scaling
        scaled_data = data / np.sum(data, 0)
        # Weight calculation
        k = 1 / np.log(data.shape[0])
        F = 1 + k * np.sum(scaled_data * np.log(scaled_data), 0)
        weight = F / np.sum(F)
        return weight
