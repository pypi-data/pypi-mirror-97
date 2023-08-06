#!/usr/bin/env python
# coding: utf-8


def generate_pairs_trading_simple_corrle(look_backs, keep_same_position_periods_list, correlation_threshold_list, suffixes_list):
    parameters = []
    for look_back in look_backs:
        for keep_same_position_periods in keep_same_position_periods_list:
            for correlation_threshold in correlation_threshold_list:
                for suffixes in suffixes_list:
                    parameters.append({
                        'lookback_window': look_back,
                        'keep_same_position_periods': keep_same_position_periods,
                        'correlation_threshold': correlation_threshold,
                        'suffixes' : suffixes})
    return parameters

def generate_pair_trading_shifted_correlation(look_backs, correlation_ranges, keep_same_position_periods_list, variants_list, suffixes_list):
    parameters = []
    for look_back in look_backs:
        for correlation_range in correlation_ranges:
            for suffixes in suffixes_list:
                for keep_same_position_periods in keep_same_position_periods_list:
                    for variant in variants_list:
                        if look_back > correlation_range:
                            parameters.append({
                                'lookback_window': look_back,
                                'correlation_range' : correlation_range,
                                'keep_same_position_periods': keep_same_position_periods,
                                'variant': variant,
                                'suffixes': suffixes})
    return parameters

def pair_trading_shifted_correlation_with_cointegration(look_backs, correlation_ranges, keep_same_position_periods_list, risk_list, alpha_list, variants_list, suffixes_list):
    parameters = []
    for look_back in look_backs:
        for correlation_range in correlation_ranges:
            for suffixes in suffixes_list:
                for keep_same_position_periods in keep_same_position_periods_list:
                    for risk in risk_list:
                        for alpha in alpha_list:
                            for variant in variants_list:
                                if look_back > correlation_range:
                                    parameters.append({
                                        'lookback_window': look_back,
                                        'correlation_range' : correlation_range,
                                        'keep_same_position_periods': keep_same_position_periods,
                                        'suffixes': suffixes,
                                        'risk': risk,
                                        'alpha': alpha,
                                        'variant': variant})
    return parameters



def generate_pairs_trading_log_simple_baseline_parameters(look_backs, keep_same_position_periods_list, percent_deviations, risk_list, alpha_list, suffixes_list):
    parameters = []
    for look_back in look_backs:
        for keep_same_position_periods in keep_same_position_periods_list:
            for percent_deviation in percent_deviations:
                for risk in risk_list:
                    for alpha in alpha_list:
                        for suffixes in suffixes_list:
                            parameters.append({
                                'lookback_window': look_back,
                                'keep_same_position_periods': keep_same_position_periods,
                                'percent_deviation': percent_deviation,
                                'risk': risk,
                                'alpha': alpha,
                                'suffixes' : suffixes})
    return parameters

def generate_pairs_trading_log_zscore_baseline_parameters(look_back_windows, keep_same_position_periods_list, risk_list, alpha_list, skipping_point_list, threshold_type_list, suffixes_list, number_of_zscore_dev_list):
    parameters = []
    for look_back_window in look_back_windows:
        for keep_same_position_periods in keep_same_position_periods_list:
            for risk in risk_list:
                for alpha in alpha_list:
                    for skipping_point in skipping_point_list:
                        for threshold_type in threshold_type_list:
                            for suffixes in suffixes_list:
                                for number_of_zscore_dev in number_of_zscore_dev_list:
                                    if skipping_point < look_back_window/2:
                                        parameters.append({
                                            'lookback_window': look_back_window,
                                            'keep_same_position_periods': keep_same_position_periods,
                                            'risk': risk,
                                            'alpha': alpha,
                                            'skipping_point': skipping_point,
                                            'threshold_type': threshold_type,
                                            'suffixes': suffixes,
                                            'number_of_zscore_dev': number_of_zscore_dev})
    return parameters

def generate_pairs_trading_log_ecm_baseline_a(look_back_windows, keep_same_position_periods_list, risk_list, alpha_list, mean_lag_list, ecm_shift_list, suffixes_list):
    parameters = []
    for look_back_window in look_back_windows:
        for keep_same_position_periods in keep_same_position_periods_list:
            for risk in risk_list:
                for alpha in alpha_list:
                    for mean_lag in mean_lag_list:
                        for ecm_shift in ecm_shift_list:
                            for suffixes in suffixes_list:
                                if mean_lag < 0.7 * look_back_window:
                                    parameters.append({
                                        'lookback_window': look_back_window,
                                        'keep_same_position_periods': keep_same_position_periods,
                                        'risk': risk,
                                        'alpha': alpha,
                                        'mean_lag': mean_lag,
                                        'ecm_shift': ecm_shift,
                                        'suffixes': suffixes})
    return parameters


