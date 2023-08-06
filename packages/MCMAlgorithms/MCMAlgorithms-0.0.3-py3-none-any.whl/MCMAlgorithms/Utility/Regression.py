import numpy as np


def R2(y_predict, y_real):
    """
    Calculate the R2 of fitting
    :param y_predict: 1-D ndarray, the model prediction of the fitting samples
    :param y_real: 1-D ndarray, the real target of the fitting sample
    :return: (ESS, TSS, R2)
    """
    ybar = np.mean(y_real)
    ESS = np.sum((y_predict - ybar) ** 2)
    TSS = np.sum((y_real - ybar) ** 2)
    R2 = np.around(ESS / TSS, 8)
    return ESS, TSS, R2


def Criterion(y_pred, y_real, k):
    """
    Calculate the AIC and SC of fitting
    :param y_predict: 1-D ndarray, the model prediction of the fitting samples
    :param y_real: 1-D ndarray, the real target of the fitting sample
    :param k: the number of sample attribute
    :return: (AIC, SC)
    """
    e = y_real - y_pred
    n = len(e)
    same_part = 1 + np.log(2 * np.pi) + np.log(np.sum(e ** 2) / n)
    AIC = same_part + (k + 1) * 2 / n
    SC = same_part + (k + 1) * np.log(n) / n
    return AIC, SC


def MultiVarStatistic(R2, n, k):
    """
    Apply calculation for adjusted R2 and F-value statistic of regression
    :param R2: fitting R2
    :param n: the number of sample
    :param k: the number of attribute
    :return: (adjusted R2, quantile of fvalue)
    note that the significance test pass when the quantile greater thant the threshold
    """
    adjusted_R2 = 1 - (1 - R2) * (n - 1) / (n - k - 1)
    F = R2 * (n - k - 1) / (k * (1 - R2))
    return adjusted_R2, F
