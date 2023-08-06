#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.api import OLS, add_constant
from statsmodels.tsa.stattools import adfuller
import statsmodels.tsa.stattools as ts
from napoleontoolbox.signal import signal_utility



#                     HRP developed by Jeroen Bouma (https://github.com/JerBouma)                  #
# ================================================================================================ #
#                                                                                                  #
def estimate_long_run_short_run_relationships(y, x):
    """Estimates long-run and short-run cointegration relationship for series y and x.

    Uses a 2-step process to first estimate coefficients for the long-run relationship
        y_t = c + gamma * x_t + z_t

    and then the short-term relationship,
        y_t - y_(t-1) = alpha * z_(t-1) + epsilon_t,

    with z the found residuals of the first equation.

    Parameters
    ----------
    y : pd.Series
        The first time series of the pair to analyse.

    x : pd.Series
        The second time series of the pair to analyse.

    Returns
    -------
    c : float
        The constant term in the long-run relationship y_t = c + gamma * x_t + z_t. This
        describes the static shift of y with respect to gamma * x.

    gamma : float
        The gamma term in the long-run relationship y_t = c + gamma * x_t + z_t. This
        describes the ratio between the const-shifted y and x.

    alpha : float
        The alpha term in the short-run relationship y_t - y_(t-1) = alpha * z_(t-1) + epsilon. This
        gives an indication of the strength of the error correction toward the long-run mean.

    z : pd.Series
        Series of residuals z_t from the long-run relationship y_t = c + gamma * x_t + z_t, representing
        the value of the error correction term.

    """

    assert isinstance(y, pd.Series), 'Input series y should be of type pd.Series'
    assert isinstance(x, pd.Series), 'Input series x should be of type pd.Series'
    assert sum(y.isnull()) == 0, 'Input series y has nan-values. Unhandled case.'
    assert sum(x.isnull()) == 0, 'Input series x has nan-values. Unhandled case.'
    assert y.index.equals(x.index), 'The two input series y and x do not have the same index.'

    long_run_ols = OLS(y, add_constant(x), has_const=True)
    long_run_ols_fit = long_run_ols.fit()

    c, gamma = long_run_ols_fit.params
    z = long_run_ols_fit.resid

    short_run_ols = OLS(y.diff().iloc[1:], (z.shift().iloc[1:]))
    short_run_ols_fit = short_run_ols.fit()

    alpha = short_run_ols_fit.params[0]

    return c, gamma, alpha, z


def engle_granger_two_step_cointegration_test(y, x):
    """Applies the two-step Engle & Granger test for cointegration.

    First fits the long-run relationship
        y_t = c + gamma * x_t + z_t

    and then tests, by Dickey-Fuller phi=1 vs phi < 1 in
        z_t = phi * z_(t-1) + eta_t

    If this implies phi < 1, the z series is stationary is concluded to be
    stationary, and thus the series y and x are concluded to be cointegrated.
    Parameters
    ----------
    y : pd.Series
        the first time series of the pair to analyse

    x : pd.Series
        the second time series of the pair to analyse

    Returns
    -------
    dfstat : float
        The Dickey Fuller test-statistic for phi = 1 vs phi < 1 in the second equation. A more
        negative value implies the existence of stronger cointegration.

    pvalue : float
        The p-value corresponding to the Dickey Fuller test-statistic. A lower value implies
        stronger rejection of no-cointegration, thus stronger evidence of cointegration.

    """

    assert isinstance(y, pd.Series), 'Input series y should be of type pd.Series'
    assert isinstance(x, pd.Series), 'Input series x should be of type pd.Series'
    assert sum(y.isnull()) == 0, 'Input series y has nan-values. Unhandled case.'
    assert sum(x.isnull()) == 0, 'Input series x has nan-values. Unhandled case.'
    assert y.index.equals(x.index), 'The two input series y and x do not have the same index.'

    c, gamma, alpha, z = estimate_long_run_short_run_relationships(y, x)

    # NOTE: The p-value returned by the adfuller function assumes we do not estimate z first, but test
    # stationarity of an unestimated series directly. This assumption should have limited effect for high N,
    # so for the purposes of this course this p-value can be used for the EG-test. Critical values taking
    # this into account more accurately are provided in e.g. McKinnon (1990) and Engle & Yoo (1987).

    adfstat, pvalue, usedlag, nobs, crit_values, icbest = adfuller(z)

    return adfstat, pvalue, crit_values, alpha, z
#                                                                                                  #
# ================================================================================================ #


def apply_cointegration_test(data_df, risk = 10, alpha = 0.05, suffixes=('_btc', '_eth')):

    y,x = data_df['log_return'+suffixes[1]],data_df['log_return'+suffixes[0]]
    adfstat, pvalue, crit_values, alpha_ols, z = engle_granger_two_step_cointegration_test(y,x)

    if pvalue > alpha:
        return False, alpha_ols, z
    elif adfstat > crit_values[str(risk)+'%']:
        return False, alpha_ols, z
    else:
        return True, alpha_ols, z

def merge_series(ts_1, ts_2, suffixes=('_btc', '_eth')):
    pair_df = pd.merge(ts_1, ts_2, how='inner', left_index=True, right_index=True, sort=True,
                             suffixes=suffixes, copy=True, indicator=False, validate=None)
    return pair_df

def add_returns(pair_df, suffixes=('_btc', '_eth')):
    returns_df = pair_df.copy()
    returns_df['return' + suffixes[0]] = returns_df['close' + suffixes[0]].pct_change()
    returns_df['return' + suffixes[1]] = returns_df['close' + suffixes[1]].pct_change()
    returns_df = returns_df.fillna(0)
    return returns_df

def add_log_returns(pair_df, suffixes=('_btc', '_eth')):
    log_returns_df = pair_df.copy()
    log_returns_df['shifted_close'+suffixes[0]] = log_returns_df['close'+suffixes[0]].shift(1)
    log_returns_df['shifted_close'+suffixes[1]] = log_returns_df['close'+suffixes[1]].shift(1)
    # log_returns_df = log_returns_df.dropna()
    log_returns_df = log_returns_df.fillna(method='ffill')
    log_returns_df = log_returns_df.fillna(method='bfill')
    log_returns_df['log_return'+suffixes[0]] = np.log(log_returns_df['close'+suffixes[0]]) - np.log(log_returns_df['shifted_close'+suffixes[0]])
    log_returns_df['log_return'+suffixes[1]] = np.log(log_returns_df['close'+suffixes[1]]) - np.log(log_returns_df['shifted_close'+suffixes[1]])
    return log_returns_df

def compute_log_return_regressor(log_returns_df, log_regressor_kind='log_x_over_log_y', suffixes=('_btc', '_eth')):
    log_return_regressor_df = log_returns_df.copy()

    if log_regressor_kind == 'log_x_over_log_y':
        log_return_regressor_df[log_regressor_kind] = log_return_regressor_df['log_return' + suffixes[0]] / \
                                                      log_return_regressor_df['log_return' + suffixes[1]]
    else:
        log_return_regressor_df[log_regressor_kind] = log_return_regressor_df['log_return' + suffixes[1]] / \
                                                      log_return_regressor_df['log_return' + suffixes[0]]
    log_return_regressor_df = log_return_regressor_df.replace([np.inf, -np.inf], np.nan)
    log_return_regressor_df = log_return_regressor_df.fillna(method='ffill')
    return log_return_regressor_df

def log_return_regressor_half_mean_and_z_score(data_df, log_regressor_kind='log_x_over_log_y', skipping_point=5):
    log_mean_zscore_df = data_df.copy()
    log_mean_zscore_df['log_return_regressor_half_mean'] = log_mean_zscore_df[log_regressor_kind].rolling(skipping_point).mean() / 2
    log_mean_zscore_df['log_return_regressor_zscore'] = signal_utility.expanding_zscore(log_mean_zscore_df[log_regressor_kind], skipping_point=skipping_point,
                                                                                        signal_continuum_threshold=1)
    log_mean_zscore_df = log_mean_zscore_df.fillna(0)
    return log_mean_zscore_df

def compute_zscore_threshold(data_df, threshold_type='max'):
    # cur_df = data_df.copy()
    cur_df = data_df[:-1].copy()
    if threshold_type == 'max':
        row = cur_df.loc[abs(cur_df.log_return_regressor_zscore) == max(abs(cur_df.log_return_regressor_zscore))]
        zscore_threshold = row.log_return_regressor_zscore[0]
    if threshold_type == 'mean':
        zscore_threshold = cur_df.log_return_regressor_zscore.mean()
    return zscore_threshold

def add_ecm_result(data_df, alpha, residuals):
    data_df['ecm'] = alpha*residuals
    return data_df

