from napoleontoolbox.cointegration_utils.cointegration_utils_numpy import utilities
import numpy as np
from npxlogger import log

def pairs_trading_simple_correlation(x_close=None, y_close = None, correlation_threshold = 0.2, **kwargs):
    try:
        assert len(y_close) == len(x_close)
    except:
        log.error('The two series must be of same length')

    x_log_return, y_log_return = utilities.log_return(x_close, y_close)
    y_cum_ret = np.sum(y_log_return)
    x_cum_ret = np.sum(x_log_return)

    correlation_matrix = np.corrcoef(x_log_return, y_log_return)
    corr_coef = correlation_matrix[0][1]
    trend = np.sign(corr_coef)
    magnitude = np.abs(corr_coef)

    if magnitude >= correlation_threshold:
        if trend == 1:
            if x_cum_ret > y_cum_ret:
                return -1, 1
            else:
                return 1, -1
        else:
            if x_cum_ret > y_cum_ret:
                return 1, -1
            else:
                return -1, 1
    else:
        return np.NaN, np.NaN

def pair_trading_shifted_correlation(x_close=None, y_close = None, correlation_range = 100, **kwargs):
    try:
        assert len(y_close) == len(x_close)
    except:
        log.error('The two series must be of same length')
    try:
        assert len(y_close) > correlation_range
    except:
        log.error('correlation range must have a lower length than the time series')

    x_return, y_return = utilities.simple_return(x_close, y_close)
    correlation_dico = {shift: value for shift in range(correlation_range) for value in
                        [np.corrcoef(y_close, np.concatenate([np.zeros(shift), utilities.check_shift(x_close, shift)]))[0][1]]}

    lag = max(correlation_dico, key=correlation_dico.get)

    if lag == 0:
        signal = np.mean(x_return[:])
        return np.sign(signal), -np.sign(signal)
    else:
        signal = np.mean(x_return[-lag])
        return -np.sign(signal), np.sign(signal)

def pair_trading_shifted_correlation_with_cointegration(x_close=None, y_close = None, correlation_range = 100, risk = 10, alpha = 0.05, **kwargs):
    try:
        assert len(y_close) == len(x_close)
    except:
        log.error('The two series must be of same length')
    try:
        assert len(y_close) > correlation_range
    except:
        log.error('correlation range must have a lower length than the time series')

    x_log_return, y_log_return = utilities.log_return(x_close, y_close)
    coint_test_result, alpha_test, z = utilities.cointegration_test(x_log_return, y_log_return, risk=risk, alpha=alpha)

    if not coint_test_result:
        x_return, y_return = utilities.simple_return(x_close, y_close)
        correlation_dico = {shift: value for shift in range(correlation_range) for value in
                            [np.corrcoef(y_close,
                                         np.concatenate([np.zeros(shift), utilities.check_shift(x_close, shift)]))[0][
                                 1]]}

        lag = max(correlation_dico, key=correlation_dico.get)
        if lag == 0:
            signal = np.mean(x_return[:])
            return np.sign(signal), -np.sign(signal)
        else:
            signal = np.mean(x_return[-lag])
            return -np.sign(signal), np.sign(signal)
    else:
        return np.NaN, np.NaN

def pairs_trading_log_simple_baseline_a(x_close=None, y_close = None, percent_deviation = 0.1, risk = 10, alpha = 0.05, **kwargs):
    try:
        assert len(y_close) == len(x_close)
    except:
        log.error('The two series must be of same length')

    x_log_return, y_log_return = utilities.log_return(x_close, y_close)
    coint_test_result, alpha_test, z = utilities.cointegration_test(x_log_return, y_log_return, risk=risk, alpha=alpha)

    if not coint_test_result:
        log_regressor = utilities.log_return_regressor(x_log_return, y_log_return)
        log_regressor = np.nan_to_num(log_regressor)
        recent_reg_value = log_regressor[-1]
        last_average_reg_value = np.mean(log_regressor[:-1])
        if recent_reg_value > (1 + percent_deviation) * last_average_reg_value:
            return -1,1

        elif recent_reg_value < (1 - percent_deviation) * last_average_reg_value:
            return 1,-1
        else:
            return np.NaN, np.NaN
    else:
        return np.NaN, np.NaN

def pairs_trading_log_simple_baseline_b(x_close=None, y_close = None, percent_deviation = 0.1, risk = 10, alpha = 0.05, **kwargs):
    try:
        assert len(y_close) == len(x_close)
    except:
        log.error('The two series must be of same length')

    x_log_return, y_log_return = utilities.log_return(x_close, y_close)
    coint_test_result, alpha_test, z = utilities.cointegration_test(x_log_return, y_log_return, risk=risk, alpha=alpha)

    if not coint_test_result:
        log_regressor = utilities.log_return_regressor(x_log_return, y_log_return)
        log_regressor = np.nan_to_num(log_regressor)
        recent_reg_value = log_regressor[-1]
        last_average_reg_value = np.mean(log_regressor[:-1])
        if recent_reg_value > (1 + percent_deviation) * last_average_reg_value:
            return -np.abs(recent_reg_value), np.abs(recent_reg_value)

        elif recent_reg_value < (1 - percent_deviation) * last_average_reg_value:
            return np.abs(recent_reg_value), -np.abs(recent_reg_value)
        else:
            return np.NaN, np.NaN
    else:
        return np.NaN, np.NaN

def pairs_trading_log_zscore_baseline_a(x_close=None, y_close=None, risk = 10, alpha = 0.05, skipping_point=5, threshold_type = 'mean', number_of_zscore_dev = 1, **kwargs):
    try:
        assert len(y_close) == len(x_close)
    except:
        log.error('The two series must be of same length')

    x_log_return, y_log_return = utilities.log_return(x_close, y_close)
    coint_test_result, alpha_test, z = utilities.cointegration_test(x_log_return, y_log_return, risk=risk, alpha=alpha)

    if not coint_test_result:
        log_regressor = utilities.log_return_regressor(x_log_return, y_log_return)
        log_regressor = np.nan_to_num(log_regressor)
        regressor_rolling_half_mean = utilities.expanding_rolling_mean(log_regressor,rolling_window=skipping_point) / 2
        regressor_rolling_half_mean = np.nan_to_num(regressor_rolling_half_mean)
        regressor_rolling_zscore = utilities.expanding_rolling_zscore(log_regressor,skipping_point=skipping_point)
        previous_half_mean = regressor_rolling_half_mean[:-1][-1]
        zscore_threshold = utilities.zscore_threshold(regressor_rolling_zscore,threshold_type=threshold_type)
        new_zscore = regressor_rolling_zscore[-1]

        if zscore_threshold >= previous_half_mean:
            if new_zscore >= number_of_zscore_dev * zscore_threshold:
                return -1,1
            else:
                return np.NaN, np.NaN

        else:
            if new_zscore <= number_of_zscore_dev * zscore_threshold:
                return 1, -1
            else:
                return np.NaN, np.NaN
    else:
        return np.NaN, np.NaN


def pairs_trading_log_zscore_baseline_b(x_close=None, y_close=None, risk = 10, alpha = 0.05, skipping_point=5, threshold_type = 'mean', number_of_zscore_dev = 1, **kwargs):
    try:
        assert len(y_close) == len(x_close)
    except:
        log.error('The two series must be of same length')

    x_log_return, y_log_return = utilities.log_return(x_close, y_close)
    coint_test_result, alpha_test, z = utilities.cointegration_test(x_log_return, y_log_return, risk=risk, alpha=alpha)

    if not coint_test_result:
        log_regressor = utilities.log_return_regressor(x_log_return, y_log_return)
        log_regressor = np.nan_to_num(log_regressor)
        recent_reg_value = log_regressor[-1]
        regressor_rolling_half_mean = utilities.expanding_rolling_mean(log_regressor,rolling_window=skipping_point) / 2
        regressor_rolling_half_mean = np.nan_to_num(regressor_rolling_half_mean)
        regressor_rolling_zscore = utilities.expanding_rolling_zscore(log_regressor,skipping_point=skipping_point)
        previous_half_mean = regressor_rolling_half_mean[:-1][-1]
        zscore_threshold = utilities.zscore_threshold(regressor_rolling_zscore,threshold_type=threshold_type)
        new_zscore = regressor_rolling_zscore[-1]

        if zscore_threshold >= previous_half_mean:
            if new_zscore >= number_of_zscore_dev * zscore_threshold:
                return -np.abs(recent_reg_value),np.abs(recent_reg_value)

        else:
            if new_zscore <= number_of_zscore_dev * zscore_threshold:
                return np.abs(recent_reg_value), -np.abs(recent_reg_value)
    else:
        return np.NaN, np.NaN

def pairs_trading_log_ecm_baseline_a(x_close=None, y_close=None, risk = 10, alpha = 0.05, mean_lag = 5, ecm_shift = 0.05, **kwargs):
    try:
        assert len(y_close) == len(x_close)
    except:
        log.error('The two series must be of same length')

    x_log_return, y_log_return = utilities.log_return(x_close, y_close)
    coint_test_result, alpha_test, z = utilities.cointegration_test(x_log_return, y_log_return, risk=risk, alpha=alpha)

    if not coint_test_result:
        error_correction = utilities.ecm_result(alpha_test, z)
        ecm_rolling_mean = utilities.expanding_rolling_mean(error_correction,rolling_window=mean_lag)
        previous_average_ecm = ecm_rolling_mean[:-1][-1]
        new_ecm = error_correction[-1]

        if new_ecm >= 0:
            if new_ecm >= previous_average_ecm + ecm_shift:
                return -1,1
            else:
                return np.NaN, np.NaN
        else:
            if new_ecm <= previous_average_ecm - ecm_shift:
                return 1,-1
            else:
                return np.NaN, np.NaN
    else:
        return np.NaN, np.NaN


def pairs_trading_log_ecm_baseline_b(x_close=None, y_close=None, risk=10, alpha=0.05, mean_lag=5, ecm_shift=0.05, **kwargs):
    try:
        assert len(y_close) == len(x_close)
    except:
        log.error('The two series must be of same length')

    x_log_return, y_log_return = utilities.log_return(x_close, y_close)
    coint_test_result, alpha_test, z = utilities.cointegration_test(x_log_return, y_log_return, risk=risk, alpha=alpha)

    if not coint_test_result:
        print('here')
        log_regressor = utilities.log_return_regressor(x_log_return, y_log_return)
        log_regressor = np.nan_to_num(log_regressor)
        recent_reg_value = log_regressor[-1]
        error_correction = utilities.ecm_result(alpha_test, z)
        ecm_rolling_mean = utilities.expanding_rolling_mean(error_correction, rolling_window=mean_lag)
        previous_average_ecm = ecm_rolling_mean[:-1][-1]
        new_ecm = error_correction[-1]

        if new_ecm >= 0:
            if new_ecm >= previous_average_ecm + ecm_shift:
                return -np.abs(recent_reg_value), np.abs(recent_reg_value)
            else:
                return np.NaN, np.NaN
        else:
            if new_ecm <= previous_average_ecm - ecm_shift:
                return np.abs(recent_reg_value), -np.abs(recent_reg_value)
            else:
                return np.NaN, np.NaN
    else:
        return np.NaN, np.NaN


if __name__ == '__main__':
    import pandas as pd
    l = 58
    y = pd.read_pickle('STOXX_03_Jan_2000_10_Mar_2020_daily_returns.pkl')[-2*l:-l]
    x = pd.read_pickle('SnP_03_Jan_2000_10_Mar_2020_daily_returns.pkl')[-2*l:-l]
    a,b = pairs_trading_log_ecm_baseline_a(x_close=x.close.values, y_close=y.close.values)
    log.info(a)
    log.info(b)
