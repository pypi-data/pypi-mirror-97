from abc import ABC, abstractmethod

import pandas as pd

from napoleontoolbox.file_saver import dropbox_file_saver
from napoleontoolbox.utility import metrics

from napoleontoolbox.signal import signal_generator
from napoleontoolbox.signal import signal_utility
from napoleontoolbox.cointegration_utils import cointegration_utilities, cointegration_signal_generator

class AbstractRunner(ABC):
    def __init__(self, starting_date = None, running_date = None, drop_token=None, dropbox_backup = True, underlying_x = None, underlying_y = None, shift_to_previous_close_underlying_x = False, shift_to_open_underlying_y = False, freqly_pkl_file_name_suffix='freqly_candels.pkl', local_root_directory='../data/', user = 'napoleon',period=252):
        super().__init__()
        self.freqly_pkl_file_name_suffix=freqly_pkl_file_name_suffix
        self.underlying_x = underlying_x
        self.underlying_y = underlying_y
        self.local_root_directory=local_root_directory
        self.dates_stub = starting_date.strftime('%d_%b_%Y') + '_' + running_date.strftime('%d_%b_%Y')
        self.saving_return_path_x = self.local_root_directory+self.underlying_x+ '_' + self.dates_stub + self.freqly_pkl_file_name_suffix
        self.saving_return_path_y = self.local_root_directory + self.underlying_y + '_' + self.dates_stub + self.freqly_pkl_file_name_suffix
        self.user=user
        self.dropbox_backup = dropbox_backup
        self.dbx = dropbox_file_saver.NaPoleonDropboxConnector(drop_token=drop_token,dropbox_backup=dropbox_backup)
        self.running_date = running_date
        self.starting_date = starting_date
        self.period = period
        self.x_suffixe, self.y_suffixe = '_'+underlying_x,'_'+underlying_y
        self.suffixes = (self.x_suffixe, self.y_suffixe)
        self.shift_to_previous_close_underlying_x = shift_to_previous_close_underlying_x
        self.shift_to_open_underlying_y = shift_to_open_underlying_y

    @abstractmethod
    def runTrial(self,saver, seed, trigger, signal_type, idios_string, transaction_costs, normalization):
        pass

class CointegrationRunner(AbstractRunner):
    def runTrial(self, saver, seed, trigger, signal_type, idios_string, transaction_costs, normalization):
        saving_key, idios = saver.create_saving_key(seed, trigger, signal_type, idios_string, transaction_costs,normalization)
        check_run_existence, table_number = saver.checkRunExistence(saving_key)
        exhaustive_check_run_existence, exhaustive_table_number = saver.exhaustiveCheckRunExistence(saving_key)
        assert check_run_existence == exhaustive_check_run_existence
        if check_run_existence:
            assert table_number == exhaustive_table_number
        if check_run_existence:
            return

        print('Launching computation with parameters : ' + saving_key)
        print('loading returns underlying x' + self.saving_return_path_x)
        freqly_df_x = pd.read_pickle(self.saving_return_path_x)
        if self.shift_to_previous_close_underlying_x:
            freqly_df_x = freqly_df_x.shift()
            freqly_df_x = freqly_df_x.dropna()
        print('loading returns underlying y' + self.saving_return_path_y)
        freqly_df_y = pd.read_pickle(self.saving_return_path_y)
        if self.shift_to_open_underlying_y:
            freqly_df_y[['close', 'open']] = freqly_df_y[['open', 'close']]

        print('merging returns x and y')
        freqly_df = cointegration_utilities.merge_series(freqly_df_x, freqly_df_y, suffixes=self.suffixes)

        print('number of duplicated dates')
        print(freqly_df.index.duplicated().sum())
        freqly_df = freqly_df.sort_index()
        print('time range before filtering ')
        print(max(freqly_df.index))
        print(min(freqly_df.index))
        try:
            freqly_df = freqly_df[freqly_df.index >= self.starting_date]
            freqly_df = freqly_df[freqly_df.index <= self.running_date]
        except:
            freqly_df.index = pd.to_datetime(freqly_df.index)
            freqly_df = freqly_df[freqly_df.index >= self.starting_date]
            freqly_df = freqly_df[freqly_df.index <= self.running_date]
        print('time range after filtering ')
        print(max(freqly_df.index))
        print(min(freqly_df.index))
        print(idios)
        if signal_type == 'long_only':
            freqly_df['signal'] = 1.
        else:
            lookback_window = idios['lookback_window']
            keep_same_position_periods = idios['keep_same_position_periods']
            skipping_size = lookback_window
            signal_generation_method_to_call = getattr(cointegration_signal_generator, signal_type)
            try:
                freqly_df = signal_utility.roll_cointegration_wrapper(freqly_df, lookback_window, keep_same_position_periods, skipping_size,
                                                        lambda x: signal_generation_method_to_call(pair_df=x, **idios),
                                                        trigger, self.suffixes)
            except Exception as inst:
                print('Trouble backtesting signal')
                print(inst)
                return

        udl_x_columns = [col for col in freqly_df.columns if self.underlying_x in col]
        udl_y_columns = [col for col in freqly_df.columns if self.underlying_y in col]
        freqly_df_x = freqly_df[udl_x_columns]
        freqly_df_y = freqly_df[udl_y_columns]
        freqly_df_x.columns = freqly_df_x.columns.str.rstrip(self.x_suffixe)
        freqly_df_y.columns = freqly_df_y.columns.str.rstrip(self.y_suffixe)

        freqly_df_x, _ = signal_utility.reconstitute_signal_perf(data=freqly_df_x, transaction_cost=transaction_costs,
                                                               normalization=normalization)
        freqly_df_y, _ = signal_utility.reconstitute_signal_perf(data=freqly_df_y, transaction_cost=transaction_costs,
                                                                 normalization=normalization)

        merged_df = cointegration_utilities.merge_series(freqly_df_x, freqly_df_y, suffixes=self.suffixes)
        freqly_df = freqly_df[['signal']]
        freqly_df = pd.merge(freqly_df,merged_df,left_index=True, right_index=True)
        freqly_df['close_return'] = freqly_df['close_return' + self.x_suffixe] + freqly_df['close_return' + self.y_suffixe]
        freqly_df['perf_return'] = freqly_df['perf_return' + self.x_suffixe] + freqly_df['perf_return' + self.y_suffixe]
        freqly_df['non_adjusted_perf_return'] = freqly_df['non_adjusted_perf_return' + self.x_suffixe] + freqly_df['non_adjusted_perf_return' + self.y_suffixe]
        freqly_df['reconstituted_perf'] = freqly_df['reconstituted_perf' + self.x_suffixe] + freqly_df['reconstituted_perf' + self.y_suffixe]

        freqly_df['perf_return'] = freqly_df_x['perf_return'] + freqly_df_y['perf_return']
        freqly_df['close_return'] = freqly_df_x['close_return'] + freqly_df_y['close_return']

        sharpe_strat = metrics.sharpe(freqly_df['perf_return'].dropna(), period=self.period, from_ret=True)
        sharpe_under = metrics.sharpe(freqly_df['close_return'].dropna(), period=self.period, from_ret=True)
        freqly_df = freqly_df.dropna()

        print('underlying pair {} sharpe'.format((self.underlying_x, self.underlying_y)))
        print(sharpe_under)
        print('strat sharpe')
        print(sharpe_strat)
        print('size before dropping duplicates')
        print(freqly_df.shape)
        freqly_df = freqly_df.drop_duplicates()
        print('size after dropping duplicates')
        print(freqly_df.shape)
        saver.saveAll(saving_key, freqly_df)
        print('save done')
        return

