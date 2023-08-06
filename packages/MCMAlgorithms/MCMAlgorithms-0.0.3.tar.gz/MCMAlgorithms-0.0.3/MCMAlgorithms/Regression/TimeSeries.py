import numpy as np


class GreyPrediction:

    def __init__(self, alpha=0.5, inspect=False):
        """
        The setting of grey prediction
        :param alpha: the coefficient of neighbour adding, with default as 0.5, float in (0, 1)
        :param inspect: whether need to inspect GM(1, 1) is useful, with default as False, boolean
                        attention: when the data does not pass the inspection, the program will throw an assertion error
        """
        self.__alpha = 1e-10 if alpha <= 0 else (0.999999999999 if alpha >= 1 else alpha)
        self.__inspect = True if inspect else False

    def fit(self, x):
        """
        Apply GM(1, 1) Prediction Fitting
        :param x: sequence, list of numbers, 1-D ndarray or torch tensor
        :return: prediction state, which may be 'Good', 'Normal' or 'Not Good'
        """
        # Inspect usage
        x = np.array(x).squeeze()
        n = len(x)
        lower_bound = np.exp(-2 / (n + 1))
        upper_bound = np.exp(23 / (n + 1))
        if self.__inspect:
            for idx in range(n - 1):
                assert lower_bound < x[idx] / x[idx + 1] < upper_bound
        # Fit coefficient
        x1 = np.cumsum(x)
        z = self.__alpha * x1[1:] + (1 - self.__alpha) * x1[:-1]
        z = z.reshape(-1, 1)
        B = np.hstack((-z, np.ones_like(z)))
        Y = x[1:].reshape(-1, 1)
        u = np.matmul(np.matmul(np.linalg.inv(np.matmul(B.T, B)), B.T), Y).squeeze()
        self.__a, self.__b = u.tolist()
        self.__data = x
        # Exam the performance
        x1_prediction = (x[0] - self.__b / self.__a) * np.exp(-self.__a * np.arange(n - 1)) + self.__b / self.__a
        x1_prediction = np.hstack((x[0], x1_prediction))
        x_prediction = np.diff(x1_prediction)
        x_prediction = np.hstack((x[0], x_prediction))
        epsilon = np.abs((x - x_prediction) / x)
        state = 'Not Good' if True in epsilon >= 0.2 else ('Normal' if True in epsilon >= 0.1 else 'Good')
        return state

    def predict(self, step=10):
        """
        Apply gm(1, 1) Prediction
        :param step: the step to predict, with default as 10, positive int
        :return: prediction result, 1-D ndarray
        """
        x = self.__data
        n = len(x)
        x1_prediction = (x[0] - self.__b / self.__a) * np.exp(-self.__a * np.arange(n + step)) + self.__b / self.__a
        x1_prediction = np.hstack((x[0], x1_prediction))
        x_prediction = np.diff(x1_prediction)
        prediction = x_prediction[n:]
        return prediction