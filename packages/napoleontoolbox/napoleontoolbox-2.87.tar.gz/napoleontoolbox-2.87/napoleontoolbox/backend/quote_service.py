__author__ = "hugo.inzirillo"

from itertools import product
from typing import List

from bifrost import NapoleonQuoteServiceConnector
from pandas import Timestamp, Timedelta
from datetime import time
from napoleontoolbox.models.filter import EodQuoteFilter
from napoleontoolbox.models.product import EodQuoteProductCodeBuilder
from napoleontoolbox.models.quote import EodQuote


class NapoleonQuoteService(object):
    def __init__(self):
        self.__quote_connector = NapoleonQuoteServiceConnector()

    @property
    def position_connector(self):
        return self.__quote_connector

    def filter(self, filter: EodQuoteFilter) -> List[EodQuote]:
        return [EodQuote().from_dict(quote) for quote in self.position_connector.filter(data=filter)]

    def __check_filter(self, filter: EodQuoteFilter):
        start_date = Timestamp(filter.minDate)
        end_date = Timestamp(filter.maxDate)
        if end_date - start_date < 1:
            return True
        else:
            raise RuntimeError("Cannot request more than 1 year by request")
