__author__ = "hugo.inzirillo"

from collections import OrderedDict
from dataclasses import dataclass
from typing import List

from arch import arch_model
from pandas import Timestamp, Series, DataFrame
from pandas._libs.tslibs.timedeltas import Timedelta
from statsmodels.stats.diagnostic import acorr_lm

from napoleontoolbox.garch_models.dataloader import NapoleonDataLoader, NapoleonDataLoaderParams
from napoleontoolbox.garch_models.plot import tsplot
from napoleontoolbox.garch_models.stats_factory import ArchTestResult
from napoleontoolbox.models.quote import EodQuote
from napoleontoolbox.utils.factory import EodQuoteFactory


@dataclass(frozen=True)
class GarchEstimationParams(object):
    start_date: Timestamp = None
    end_date: Timestamp = None
    underlyings: List[str] = None
    quotes: List[EodQuote] = None
    p: int = 1
    o: int = 0
    q: int = 1


@dataclass(frozen=True)
class GarchEstimationResult(object):
    pass


class GarchEstimation(object):
    def __init__(self, params: GarchEstimationParams):
        self.__quotes = OrderedDict()
        self.__parameters = params
        GarchEstimation.__post_init__(self)

    def __post_init__(self):
        self.__load_data()

    @property
    def quotes(self):
        return self.__quotes

    def get_returns(self):
        prices = Series(self.quotes).sort_index()
        return (prices / prices.shift(1) - 1).dropna()

    def ts_plot(self):
        return tsplot(self.get_returns(), lags=20)

    @property
    def parameters(self):
        return self.__parameters

    def get_epsilon_squared(self):
        s = Series(self.quotes).sort_index()
        return (((s / s.shift(1) - 1) - (s / s.shift(1) - 1).mean()) ** 2).dropna()

    def __load_data(self):
        if self.__parameters.quotes is None:
            dataloader_params = NapoleonDataLoaderParams(self.__parameters.start_date, self.__parameters.end_date,
                                                         self.__parameters.underlyings)
            quotes = NapoleonDataLoader(dataloader_params).quotes
            if quotes is not None:
                self.__quotes = EodQuoteFactory().to_ordered_dict(quotes)
            else:
                raise Exception("Quote is none type : credentials should be checked")
        else:
            self.__quotes = EodQuoteFactory().to_ordered_dict(self.__parameters.quotes)
        return self

    def residuals_autocorr_test(self):
        lm_stat, lm_pval, f_stat, f_val = acorr_lm(self.get_epsilon_squared().values, nlags=20)
        res = ArchTestResult(lm_stat, lm_pval, f_stat, f_val)
        return DataFrame.from_dict(res.__dict__, orient="index")

    def garch_estimation(self):
        garch = arch_model(self.get_returns() * 100, vol='GARCH', p=self.__parameters.p, q=self.__parameters.q,
                           dist="Normal")
        DataFrame([self.get_returns().rolling(window=10).std(), garch.fit().conditional_volatility]).transpose().plot()
        df = DataFrame(self.get_returns().rolling(window=10).std().dropna()).join(
            garch.fit().conditional_volatility / 100)
        signals = (df[0] - df['cond_vol'] > 0).map(lambda x: -1 if x == True else 1)
        returns = OrderedDict(self.get_returns().to_dict())
        strat_returns = OrderedDict({date: signals.get(date - Timedelta(hours=1)) * returns.get(date) for date, ret in
                         returns.items() if signals.get(date - Timedelta(hours=1)) is not None})

        levels = OrderedDict()
        levels[min(strat_returns.keys())] = self.quotes.get(min(strat_returns.keys()))
        for date,expected_return in strat_returns.items():
            if not date in levels:
                levels[date]=levels.get(date-Timedelta(hours=1))*(1+strat_returns.get(date))

if __name__ == '__main__':
    params = GarchEstimationParams(
        start_date=Timestamp.utcnow() - Timedelta(days=360),
        end_date=Timestamp.utcnow() - Timedelta(minutes=1),
        underlyings=["ETH-USD"]
    )
    garch = GarchEstimation(params)
    # garch.ts_plot()
    # arch_test = garch.residuals_autocorr_test()
    estimation = garch.garch_estimation()
    end = True
