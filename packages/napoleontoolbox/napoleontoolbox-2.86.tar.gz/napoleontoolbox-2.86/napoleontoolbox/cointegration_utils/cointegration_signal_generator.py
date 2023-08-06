#!/usr/bin/env python
# coding: utf-8

from napoleontoolbox.cointegration_utils import cointegration_utilities
import numpy as np

# MAX_PERIOD_TO_KEEP_POSITION = 0
# PREVIOUS_SIGNAL_TYPE = None


def pairs_trading_simple_correlation(pair_df = None, correlation_threshold = 0.2, suffixes=('_btc', '_eth'), **kwargs):
    log_returns_df = cointegration_utilities.add_log_returns(pair_df, suffixes=suffixes)
    y,x = log_returns_df['log_return'+suffixes[1]],log_returns_df['log_return'+suffixes[0]]

    y_cum_ret = log_returns_df['log_return' + suffixes[1]].sum()
    x_cum_ret = log_returns_df['log_return' + suffixes[0]].sum()

    correlation_matrix = np.corrcoef(x, y)
    corr_coef = correlation_matrix[0][1]
    trend = np.sign(corr_coef)
    magnitude = abs(corr_coef)

    if magnitude >= correlation_threshold:
        if trend == 1:
            if x_cum_ret>y_cum_ret:
                return -1,1
            else :
                return 1,-1
        else:
            if x_cum_ret>y_cum_ret:
                return 1,-1
            else :
                return -1,1
    else:
        np.nan,np.nan

    return None


def pair_trading_shifted_correlation(pair_df = None, correlation_range = 100, variant = 'a', suffixes=('_btc', '_eth'), **kwargs):
    len_histo = len(pair_df)
    assert len_histo > correlation_range
    return_pair_df = cointegration_utilities.add_returns(pair_df, suffixes=suffixes)
    correlation_dico = {}
    for shift in range(correlation_range):
        shifted_df = return_pair_df.shift(shift).copy()
        shifted_df['return' + suffixes[0]] = return_pair_df['return'+suffixes[0]].shift(shift)
        correlation_dico[shift] = shifted_df[['return'+suffixes[0], 'return'+suffixes[1]]].corr().values[0][1]
    lag = max(correlation_dico, key=correlation_dico.get)
    if variant == 'a':
        signal = return_pair_df['return' + suffixes[0]].values[-lag]
        # return -np.sign(signal), np.sign(signal)
        return 0, np.sign(signal)

    elif variant == 'b':
        signal = np.mean(return_pair_df['return' + suffixes[0]].values[-lag:])
        # return np.sign(signal), -np.sign(signal)
        return 0, -np.sign(signal)

def pair_trading_shifted_correlation_with_cointegration(pair_df = None, correlation_range = 100, risk = 10, alpha = 0.05, variant = 'a', suffixes=('_btc', '_eth'), **kwargs):
    len_histo = len(pair_df)
    assert len_histo > correlation_range
    log_returns_df = cointegration_utilities.add_log_returns(pair_df, suffixes=suffixes)
    log_returns_df = cointegration_utilities.compute_log_return_regressor(log_returns_df, suffixes=suffixes)
    return_pair_df = cointegration_utilities.add_returns(log_returns_df, suffixes=suffixes)
    coint_test, alpha, z = cointegration_utilities.apply_cointegration_test(return_pair_df, risk=risk, alpha=alpha,
                                                                            suffixes=suffixes)
    if not coint_test:
        correlation_dico = {}
        for shift in range(correlation_range):
            shifted_df = return_pair_df.shift(shift).copy()
            shifted_df['return' + suffixes[0]] = return_pair_df['return'+suffixes[0]].shift(shift)
            correlation_dico[shift] = shifted_df[['return'+suffixes[0], 'return'+suffixes[1]]].corr().values[0][1]
        lag = max(correlation_dico, key=correlation_dico.get)

        if variant == 'a':
            signal = return_pair_df['return'+suffixes[0]].values[-lag]
            # return -np.sign(signal), np.sign(signal)
            return 0, np.sign(signal)

        elif variant == 'b':
            signal = np.mean(return_pair_df['return'+suffixes[0]].values[-lag:])
            # return np.sign(signal), -np.sign(signal)
            return 0, -np.sign(signal)
    else:
        return np.nan,np.nan


def pairs_trading_log_simple_baseline_a(pair_df=None, percent_deviation = 0.1, risk = 10, alpha = 0.05, suffixes=('_btc', '_eth'), log_regressor_kind='log_x_over_log_y', **kwargs):
    log_returns_df = cointegration_utilities.add_log_returns(pair_df, suffixes=suffixes)
    log_returns_df = cointegration_utilities.compute_log_return_regressor(log_returns_df, suffixes=suffixes)
    coint_test, alpha, z = cointegration_utilities.apply_cointegration_test(log_returns_df, risk=risk, alpha = alpha, suffixes=suffixes)
    data_df = log_returns_df.copy()

    udl_x = 'flat'
    udl_y = 'flat'
    current_signal_type = None
    # global MAX_PERIOD_TO_KEEP_POSITION, PREVIOUS_SIGNAL_TYPE

    if not coint_test: #If not cointegrated

        new_return_regressor = data_df[log_regressor_kind][-1]
        # last_mean_regressor = data_df[log_regressor_kind].mean()
        last_mean_regressor = data_df[log_regressor_kind][:-1].mean()

        actions_udl_x = {'long': 1, 'short': -1, 'flat': 0}
        actions_udl_y = {'long': 1, 'short': -1, 'flat': 0}

        if new_return_regressor>(1+percent_deviation)*last_mean_regressor:
            current_signal_type = 'new_return_regressor>threshold'
            udl_x = 'short'
            udl_y = 'long'

        elif new_return_regressor<(1-percent_deviation)*last_mean_regressor:
            current_signal_type = 'new_return_regressor<threshold'
            udl_x = 'long'
            udl_y = 'short'

        return actions_udl_x[udl_x], actions_udl_y[udl_y]
        # if PREVIOUS_SIGNAL_TYPE != current_signal_type:
        #     PREVIOUS_SIGNAL_TYPE = current_signal_type
        #     MAX_PERIOD_TO_KEEP_POSITION = 1
        #     return actions_udl_x[udl_x], actions_udl_y[udl_y]
        #
        # else:
        #     if MAX_PERIOD_TO_KEEP_POSITION > keep_same_position_periods:
        #         udl_x = 'flat'
        #         udl_y = 'flat'
        #         return actions_udl_x[udl_x], actions_udl_y[udl_y]
        #     else:
        #         MAX_PERIOD_TO_KEEP_POSITION += 1
        #         return actions_udl_x[udl_x], actions_udl_y[udl_y]
    else:
        return 0, 0


def pairs_trading_log_simple_baseline_b(pair_df=None, percent_deviation = 0.1, risk = 10, alpha = 0.05, suffixes=('_btc', '_eth'), log_regressor_kind='log_x_over_log_y', **kwargs):
    log_returns_df = cointegration_utilities.add_log_returns(pair_df, suffixes=suffixes)
    log_returns_df = cointegration_utilities.compute_log_return_regressor(log_returns_df, suffixes=suffixes)
    coint_test, alpha, z = cointegration_utilities.apply_cointegration_test(log_returns_df, risk=risk, alpha = alpha, suffixes=suffixes)
    data_df = log_returns_df.copy()

    udl_x = 'flat'
    udl_y = 'flat'
    current_signal_type = None
    # global MAX_PERIOD_TO_KEEP_POSITION, PREVIOUS_SIGNAL_TYPE

    if not coint_test: #If not cointegrated

        new_return_regressor = data_df[log_regressor_kind][-1]
        # last_mean_regressor = data_df[log_regressor_kind].mean()
        last_mean_regressor = data_df[log_regressor_kind][:-1].mean()

        actions_udl_x = {'long': 1, 'short': -1, 'flat': 0}
        actions_udl_y = {'long': abs(new_return_regressor), 'short': -abs(new_return_regressor), 'flat': 0}

        if new_return_regressor>(1+percent_deviation)*last_mean_regressor:
            current_signal_type = 'new_return_regressor>threshold'
            udl_x = 'short'
            udl_y = 'long'

        elif new_return_regressor<(1-percent_deviation)*last_mean_regressor:
            current_signal_type = 'new_return_regressor<threshold'
            udl_x = 'long'
            udl_y = 'short'

        return actions_udl_x[udl_x], actions_udl_y[udl_y]
        # if PREVIOUS_SIGNAL_TYPE != current_signal_type:
        #     PREVIOUS_SIGNAL_TYPE = current_signal_type
        #     MAX_PERIOD_TO_KEEP_POSITION = 1
        #     return actions_udl_x[udl_x], actions_udl_y[udl_y]
        #
        # else:
        #     if MAX_PERIOD_TO_KEEP_POSITION > keep_same_position_periods:
        #         udl_x = 'flat'
        #         udl_y = 'flat'
        #         return actions_udl_x[udl_x], actions_udl_y[udl_y]
        #     else:
        #         MAX_PERIOD_TO_KEEP_POSITION += 1
        #         return actions_udl_x[udl_x], actions_udl_y[udl_y]
    else:
        return 0, 0

def pairs_trading_log_zscore_baseline_a(pair_df=None, risk = 10, alpha = 0.05, skipping_point=5, threshold_type = 'mean', suffixes=('_btc', '_eth'), number_of_zscore_dev = 1, log_regressor_kind='log_x_over_log_y', **kwargs):
    log_returns_df = cointegration_utilities.add_log_returns(pair_df, suffixes=suffixes)
    log_returns_df = cointegration_utilities.compute_log_return_regressor(log_returns_df, suffixes=suffixes)
    log_mean_zscore_df = cointegration_utilities.log_return_regressor_half_mean_and_z_score(log_returns_df, log_regressor_kind=log_regressor_kind, skipping_point=skipping_point)
    data_df = log_mean_zscore_df.copy()
    coint_test, alpha, z = cointegration_utilities.apply_cointegration_test(data_df, risk=risk, alpha=alpha,
                                                                  suffixes=suffixes)
    udl_x = 'flat'
    udl_y = 'flat'
    current_signal_type = None
    # global MAX_PERIOD_TO_KEEP_POSITION, PREVIOUS_SIGNAL_TYPE

    if not coint_test: #If not cointegrated

        # last_half_mean = data_df.log_return_regressor_half_mean[-1]
        last_half_mean = data_df.log_return_regressor_half_mean[:-1][-1]
        new_zscore = data_df.log_return_regressor_zscore[-1]
        zscore_threshold = cointegration_utilities.compute_zscore_threshold(data_df, threshold_type)

        actions_udl_x = {'long': 1, 'short': -1, 'flat': 0}
        actions_udl_y = {'long': 1, 'short': -1, 'flat': 0}

        if zscore_threshold >= last_half_mean:
            if new_zscore >= number_of_zscore_dev*zscore_threshold:
                current_signal_type = 'new_zscore>zscore_threshold'
                udl_x = 'short'
                udl_y = 'long'

        else:
            if new_zscore <= number_of_zscore_dev*zscore_threshold:
                current_signal_type = 'new_zscore<zscore_threshold'
                udl_x = 'long'
                udl_y = 'short'

        return actions_udl_x[udl_x], actions_udl_y[udl_y]
        # if PREVIOUS_SIGNAL_TYPE != current_signal_type:
        #     PREVIOUS_SIGNAL_TYPE = current_signal_type
        #     MAX_PERIOD_TO_KEEP_POSITION = 1
        #     return actions_udl_x[udl_x], actions_udl_y[udl_y]
        #
        # else:
        #     if MAX_PERIOD_TO_KEEP_POSITION > keep_same_position_periods:
        #         udl_x = 'flat'
        #         udl_y = 'flat'
        #         return actions_udl_x[udl_x], actions_udl_y[udl_y]
        #     else:
        #         MAX_PERIOD_TO_KEEP_POSITION += 1
        #         return actions_udl_x[udl_x], actions_udl_y[udl_y]
    else:
        return 0, 0


def pairs_trading_log_zscore_baseline_b(pair_df=None, risk=10, alpha=0.05,
                                        skipping_point=5, threshold_type='mean', suffixes=('_btc', '_eth'),
                                        number_of_zscore_dev = 1, log_regressor_kind='log_x_over_log_y', **kwargs):
    log_returns_df = cointegration_utilities.add_log_returns(pair_df, suffixes=suffixes)
    log_returns_df = cointegration_utilities.compute_log_return_regressor(log_returns_df, suffixes=suffixes)
    log_mean_zscore_df = cointegration_utilities.log_return_regressor_half_mean_and_z_score(log_returns_df,
                                                                                            log_regressor_kind=log_regressor_kind,
                                                                                            skipping_point=skipping_point)
    data_df = log_mean_zscore_df.copy()
    coint_test, alpha, z = cointegration_utilities.apply_cointegration_test(data_df, risk=risk, alpha=alpha,
                                                                  suffixes=suffixes)
    udl_x = 'flat'
    udl_y = 'flat'
    current_signal_type = None
    # global MAX_PERIOD_TO_KEEP_POSITION, PREVIOUS_SIGNAL_TYPE

    if not coint_test:  # If not cointegrated

        # last_half_mean = data_df.log_return_regressor_half_mean[-1]
        last_half_mean = data_df.log_return_regressor_half_mean[:-1][-1]
        new_zscore = data_df.log_return_regressor_zscore[-1]
        zscore_threshold = cointegration_utilities.compute_zscore_threshold(data_df, threshold_type)
        new_return_regressor = data_df[log_regressor_kind][-1]

        actions_udl_x = {'long': 1, 'short': -1, 'flat': 0}
        actions_udl_y = {'long': abs(new_return_regressor), 'short': -abs(new_return_regressor), 'flat': 0}

        if zscore_threshold >= last_half_mean:
            if new_zscore >= number_of_zscore_dev*zscore_threshold:
                current_signal_type = 'new_zscore>zscore_threshold'
                udl_x = 'short'
                udl_y = 'long'

        else:
            if new_zscore <= number_of_zscore_dev*zscore_threshold:
                current_signal_type = 'new_zscore<zscore_threshold'
                udl_x = 'long'
                udl_y = 'short'

        return actions_udl_x[udl_x], actions_udl_y[udl_y]
        # if PREVIOUS_SIGNAL_TYPE != current_signal_type:
        #     PREVIOUS_SIGNAL_TYPE = current_signal_type
        #     MAX_PERIOD_TO_KEEP_POSITION = 1
        #     return actions_udl_x[udl_x], actions_udl_y[udl_y]
        #
        # else:
        #     if MAX_PERIOD_TO_KEEP_POSITION > keep_same_position_periods:
        #         udl_x = 'flat'
        #         udl_y = 'flat'
        #         return actions_udl_x[udl_x], actions_udl_y[udl_y]
        #     else:
        #         MAX_PERIOD_TO_KEEP_POSITION += 1
        #         return actions_udl_x[udl_x], actions_udl_y[udl_y]
    else:
        return 0, 0

def pairs_trading_log_ecm_baseline_a(pair_df=None, risk = 10, alpha = 0.05, mean_lag = 5, ecm_shift = 0.05, suffixes=('_btc', '_eth'), **kwargs):
    """ Using Error Correction Model """
    log_returns_df = cointegration_utilities.add_log_returns(pair_df, suffixes=suffixes)
    log_returns_df = cointegration_utilities.compute_log_return_regressor(log_returns_df, suffixes=suffixes)
    data_df = log_returns_df.copy()
    coint_test, alpha, z = cointegration_utilities.apply_cointegration_test(data_df, risk=risk, alpha=alpha,
                                                                            suffixes=suffixes)
    data_df = cointegration_utilities.add_ecm_result(data_df, alpha, z)

    udl_x = 'flat'
    udl_y = 'flat'
    current_signal_type = None
    # global MAX_PERIOD_TO_KEEP_POSITION, PREVIOUS_SIGNAL_TYPE

    if not coint_test:  # If not cointegrated
        # last_moving_average_ecm = data_df.ecm.rolling(mean_lag).mean()[-1]
        last_moving_average_ecm = data_df.ecm.rolling(mean_lag).mean()[:-1][-1]
        new_ecm = data_df.ecm[-1]

        actions_udl_x = {'long': 1, 'short': -1, 'flat': 0}
        actions_udl_y = {'long': 1, 'short': -1, 'flat': 0}

        if new_ecm >= 0:
            if new_ecm >= last_moving_average_ecm + ecm_shift:
                current_signal_type = 'new_ecm >= last_moving_average_ecm + ecm_shift'
                udl_x = 'short'
                udl_y = 'long'

        else:
            if new_ecm <= last_moving_average_ecm - ecm_shift:
                current_signal_type = 'new_ecm <= last_moving_average_ecm - ecm_shift'
                udl_x = 'long'
                udl_y = 'short'

        return actions_udl_x[udl_x], actions_udl_y[udl_y]
        # if PREVIOUS_SIGNAL_TYPE != current_signal_type:
        #     PREVIOUS_SIGNAL_TYPE = current_signal_type
        #     MAX_PERIOD_TO_KEEP_POSITION = 1
        #     return actions_udl_x[udl_x], actions_udl_y[udl_y]
        #
        # else:
        #     if MAX_PERIOD_TO_KEEP_POSITION > keep_same_position_periods:
        #         udl_x = 'flat'
        #         udl_y = 'flat'
        #         return actions_udl_x[udl_x], actions_udl_y[udl_y]
        #     else:
        #         MAX_PERIOD_TO_KEEP_POSITION += 1
        #         return actions_udl_x[udl_x], actions_udl_y[udl_y]
    else:
        return 0, 0


def pairs_trading_log_ecm_baseline_b(pair_df=None, risk=10, alpha=0.05, mean_lag=5, ecm_shift=0.05, suffixes=('_btc', '_eth'), log_regressor_kind='log_x_over_log_y', **kwargs):
    """ Using Error Correction Model """
    log_returns_df = cointegration_utilities.add_log_returns(pair_df, suffixes=suffixes)
    log_returns_df = cointegration_utilities.compute_log_return_regressor(log_returns_df, suffixes=suffixes)
    data_df = log_returns_df.copy()
    coint_test, alpha, z = cointegration_utilities.apply_cointegration_test(data_df, risk=risk, alpha=alpha,
                                                                            suffixes=suffixes)
    data_df = cointegration_utilities.add_ecm_result(data_df, alpha, z)

    udl_x = 'flat'
    udl_y = 'flat'
    current_signal_type = None
    # global MAX_PERIOD_TO_KEEP_POSITION, PREVIOUS_SIGNAL_TYPE

    if not coint_test:  # If not cointegrated
        # last_moving_average_ecm = data_df.ecm.rolling(mean_lag).mean()[-1]
        last_moving_average_ecm = data_df.ecm.rolling(mean_lag).mean()[:-1][-1]
        new_ecm = data_df.ecm[-1]
        new_return_regressor = data_df[log_regressor_kind][-1]

        actions_udl_x = {'long': 1, 'short': -1, 'flat': 0}
        actions_udl_y = {'long': abs(new_return_regressor), 'short': -abs(new_return_regressor), 'flat': 0}

        if new_ecm >= 0:
            if new_ecm >= last_moving_average_ecm + ecm_shift:
                current_signal_type = 'new_ecm >= last_moving_average_ecm + ecm_shift'
                udl_x = 'short'
                udl_y = 'long'

        else:
            if new_ecm <= last_moving_average_ecm - ecm_shift:
                current_signal_type = 'new_ecm <= last_moving_average_ecm - ecm_shift'
                udl_x = 'long'
                udl_y = 'short'

        return actions_udl_x[udl_x], actions_udl_y[udl_y]
        # if PREVIOUS_SIGNAL_TYPE != current_signal_type:
        #     PREVIOUS_SIGNAL_TYPE = current_signal_type
        #     MAX_PERIOD_TO_KEEP_POSITION = 1
        #     return actions_udl_x[udl_x], actions_udl_y[udl_y]
        #
        # else:
        #     if MAX_PERIOD_TO_KEEP_POSITION > keep_same_position_periods:
        #         udl_x = 'flat'
        #         udl_y = 'flat'
        #         return actions_udl_x[udl_x], actions_udl_y[udl_y]
        #     else:
        #         MAX_PERIOD_TO_KEEP_POSITION += 1
        #         return actions_udl_x[udl_x], actions_udl_y[udl_y]
    else:
        return 0, 0
