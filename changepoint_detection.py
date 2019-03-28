import numpy as np
from sklearn.metrics import mean_squared_error


def cpd(freq_count):
    """
    :param freq_count: the frequency of a word from 1900-2000
    :type freq_count: list of int
    :return: cp_year, the changepoint year
    :rtype: int(the year), float(the min mse value)
    """
    years = np.arange(0, 100, 1)
    mse = []
    for i in years:
        fit = np.polyfit(years[i:], freq_count[i:], 2)
        linefit = np.poly1d(fit)
        y_fit = np.zeros(i)
        y_fit = np.concatenate((y_fit, linefit(years[i:])), axis=0)
        mse.append(mean_squared_error(freq_count, y_fit))
    min_mse = mse.index(min(mse))
    cp_year = 1900 + min_mse
    return cp_year, mse[min_mse]
