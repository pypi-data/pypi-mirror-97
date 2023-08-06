import sys

sys.path.append('..')
import numpy as np
import scipy.stats as stats
import Utility.Regression as reg


class Linear:

    def __init__(self):
        self.__beta = None
        self.__fitted = False

    def fit(self, x, y, threshold=0.05):
        """
        Apply Linear Regression fitting
        :param x: 2-D ndarray, whose size is (M, N), M is the number of sample, N is the number of attribute
        :param y: 1-D ndarray, whose length shall be M, the array of target y of each sample
        :param threshold: scalar in (0,1), indicating the threshold of significance test
        :return: (weight: 1-D ndarray with length N + 1, weight[0] is the bias, R2: scalar in [0,1], adjusted R2: scalar in [0,1], quantile of fvalue: scalar in [0,1])
        """
        # Exam the parameter
        threshold = 0.05 if threshold <= 0 or threshold >= 1 else threshold
        # Fit the linear model parameters with OLS
        sample_num, attribute_num = x.shape
        x = np.hstack((np.ones((sample_num, 1)), x))
        y = y.squeeze()
        first_part = np.dot(x.T, x)
        second_part = np.dot(np.linalg.inv(first_part), x.T)
        self.__beta = np.dot(second_part, y.reshape(-1, 1))
        self.__fitted = True
        # Significance test
        predict_y = self.predict(x[:, 1:])
        _1, _2, R2 = reg.R2(predict_y, y)
        adjusted_R2, F = reg.MultiVarStatistic(R2, sample_num, attribute_num)
        F__threshold = stats.f.isf(threshold, attribute_num, sample_num - attribute_num - 1)
        significance = F > F__threshold
        return self.__beta.squeeze(), R2, adjusted_R2, significance

    def predict(self, x):
        """
        Apply Linear Regression prediction
        :param x: 2-D ndarray, whose size is (M, N), M is the number of sample, N is the number of weight
        :return: 1-D ndarray, the prediction output of each sample
        """
        if not self.__fitted:
            raise AssertionError('Model not fitted yet')
        x = np.hstack((np.ones((x.shape[0], 1)), x))
        return np.dot(x, self.__beta).squeeze()
