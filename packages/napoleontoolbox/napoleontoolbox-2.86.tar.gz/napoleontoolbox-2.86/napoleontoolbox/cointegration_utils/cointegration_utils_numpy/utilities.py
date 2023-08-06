#!/usr/bin/env python
# coding: utf-8

import numpy as np
from statsmodels.api import OLS, add_constant
from statsmodels.tsa.stattools import adfuller

from napoleontoolbox.cointegration_utils import cointegration_utilities
from napoleontoolbox.signal import signal_utility

from npxlogger import log


def estimate_long_run_short_run_relationships(x, y):

    try:
        assert isinstance(y, np.ndarray)
    except:
        log.error('Input series y should be of type np.ndarray')

    try:
        assert isinstance(x, np.ndarray)
    except:
        log.error('Input series x should be of type np.ndarray')

    try:
        assert np.isnan(np.sum(y)) == False
    except:
        log.error('Input series y has nan-values. Unhandled case.')

    try:
        assert np.isnan(np.sum(y)) == False
    except:
        log.error('Input series x has nan-values. Unhandled case.')

    try:
        assert len(y)==len(x)
    except:
        log.error('The two input series y and x do not have the same legnth.')

    long_run_ols = OLS(y, add_constant(x), has_const=True)
    long_run_ols_fit = long_run_ols.fit()

    c, gamma = long_run_ols_fit.params
    z = long_run_ols_fit.resid

    short_run_ols = OLS(np.diff(y), (z[:-1]))
    short_run_ols_fit = short_run_ols.fit()

    alpha = short_run_ols_fit.params[0]

    return c, gamma, alpha, z



def engle_granger_two_step_cointegration_test(x, y):

    try:
        assert isinstance(y, np.ndarray)
    except:
        log.error('Input series y should be of type np.ndarray')

    try:
        assert isinstance(x, np.ndarray)
    except:
        log.error('Input series x should be of type np.ndarray')

    try:
        assert np.isnan(np.sum(y)) == False
    except:
        log.error('Input series y has nan-values. Unhandled case.')

    try:
        assert np.isnan(np.sum(y)) == False
    except:
        log.error('Input series x has nan-values. Unhandled case.')

    try:
        assert len(y) == len(x)
    except:
        log.error('The two input series y and x do not have the same legnth.')

    c, gamma, alpha, z = estimate_long_run_short_run_relationships(x, y)

    # NOTE: The p-value returned by the adfuller function assumes we do not estimate z first, but test
    # stationarity of an unestimated series directly. This assumption should have limited effect for high N,
    # so for the purposes of this course this p-value can be used for the EG-test. Critical values taking
    # this into account more accurately are provided in e.g. McKinnon (1990) and Engle & Yoo (1987).

    adfstat, pvalue, usedlag, nobs, crit_values, icbest = adfuller(z)

    return adfstat, pvalue, crit_values, alpha, z

def cointegration_test(x, y, risk = 10, alpha = 0.05):

    adfstat, pvalue, crit_values, alpha_ols, z = engle_granger_two_step_cointegration_test(x,y)

    if pvalue > alpha:
        return False, alpha_ols, z
    elif adfstat > crit_values[str(risk)+'%']:
        return False, alpha_ols, z
    else:
        return True, alpha_ols, z

def simple_return(x_close, y_close):
    y_return = np.concatenate([np.array([np.NaN]),np.diff(y_close) / y_close[:-1]])
    x_return = np.concatenate([np.array([np.NaN]),np.diff(x_close) / x_close[:-1]])
    y_return = np.nan_to_num(y_return)
    x_return = np.nan_to_num(x_return)
    return x_return, y_return

def log_return(x_close, y_close):
    y_log_return = np.concatenate([np.array([np.NaN]),np.diff(np.log(y_close))])
    x_log_return = np.concatenate([np.array([np.NaN]),np.diff(np.log(x_close))])
    y_log_return = np.nan_to_num(y_log_return)
    x_log_return = np.nan_to_num(x_log_return)
    return x_log_return, y_log_return

def log_return_regressor(x_log_return, y_log_return):
    log_regressor = x_log_return/y_log_return
    log_regressor[log_regressor == np.Inf] = np.NaN
    log_regressor[log_regressor == -np.Inf] = np.NaN

    arr = np.array([log_regressor])
    mask = np.isnan(arr)
    idx = np.where(~mask, np.arange(mask.shape[1]), 0)
    arr[mask] = arr[np.nonzero(mask)[0], idx[mask]]
    log_regressor = arr[0]
    return log_regressor

def ecm_result(alpha, residuals):
    return alpha*residuals

def expanding_rolling_mean(signal_np_array, rolling_window=5):
    signal_np_array = np.nan_to_num(signal_np_array)
    cumsum, moving_aves = [0], []
    for i, x in enumerate(signal_np_array, 1):
        cumsum.append(cumsum[i - 1] + x)
        if i > rolling_window:
            moving_av = (cumsum[i] - cumsum[i - rolling_window]) / rolling_window
            moving_aves.append(moving_av)
    moving_aves = np.concatenate([np.array([np.NaN]*rolling_window),moving_aves])
    return moving_aves

def expanding_rolling_zscore(signal_np_array=None, skipping_point = 5, signal_continuum_threshold = 1):
    signal_np_array = np.nan_to_num(signal_np_array)
    try:
        assert skipping_point < len(signal_np_array)
    except:
        log.error('Number of skipping point should be lower than the len of the array')
    zscore = signal_utility.expanding_zscore(signal_np_array, skipping_point=skipping_point,signal_continuum_threshold=1)
    return zscore

def zscore_threshold(my_array,threshold_type='max'):
    my_array = my_array[:-1]
    my_array = np.nan_to_num(my_array)
    if threshold_type == 'max':
        return max(my_array,key=abs)
    elif threshold_type == 'mean':
        return np.mean(my_array)

def check_shift(close, shift):
    if shift == 0:
        return close
    else:
        return close[:-shift]