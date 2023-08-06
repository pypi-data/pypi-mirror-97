__author__ = "hugo.inzirillo"

from dataclasses import dataclass
from typing import List

from pandas import Timestamp

from napoleontoolbox.backend.quote_service import NapoleonQuoteService
from napoleontoolbox.models.filter import EodQuoteFilter
from napoleontoolbox.models.product import EodQuoteProductCodeBuilder
from napoleontoolbox.models.quote import EodQuote


@dataclass
class NapoleonDataLoaderParams:
    start_date: Timestamp
    end_date: Timestamp
    underlyings: List[str]


class NapoleonDataLoader(object):
    def __init__(self, params: NapoleonDataLoaderParams):
        self.__parameters = params
        self.__quotes = List[EodQuote]
        NapoleonDataLoader.__post_init__(self)
        pass

    def __post_init__(self):
        self.__load_data()

    @property
    def quotes(self):
        return self.__quotes

    def __load_data(self):
        if self.__parameters.start_date and self.__parameters.end_date and self.__parameters.underlyings:
            filter = EodQuoteFilter(
                productCodes=EodQuoteProductCodeBuilder.product_code_generator(self.__parameters.underlyings),
                minDate=self.__parameters.start_date.strftime("%Y-%m-%d"),
                maxDate=self.__parameters.end_date.strftime("%Y-%m-%d"))
            self.__quotes = sorted(NapoleonQuoteService().filter(filter))
