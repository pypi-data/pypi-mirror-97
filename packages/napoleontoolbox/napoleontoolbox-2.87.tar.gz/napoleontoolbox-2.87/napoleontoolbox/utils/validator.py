__author__ = "hugo.inzirillo"

from pandas import Timestamp

from models.filter import SignalComputationFilter
from utils.service_exceptions import NapbotsReportingServiceValueError, \
    NapbotsReportingServiceException


class SignalComputationFilterValidator(object):
    def __init__(self, signal_filter: SignalComputationFilter):
        self.__signal_filter = signal_filter

    @property
    def signal_filter(self) -> SignalComputationFilter:
        return self.__signal_filter

    @property
    def is_valid(self) -> bool:
        return self.__validate()

    def __validate(self):
        self.__check_timestamp()

        return True

    def __check_timestamp(self):
        if self.signal_filter.lastOnly:
            pass
        elif self.signal_filter.lastOnly == False \
                and self.signal_filter.maxTs is not None \
                and self.signal_filter.minTs is not None:
            if isinstance(self.signal_filter.maxTs, Timestamp) and isinstance(self.signal_filter.minTs, Timestamp):
                self.__check_date(self.signal_filter.minTs,self.signal_filter.maxTs)
                self.signal_filter.maxTs = self.signal_filter.maxTs.strftime("%Y-%m-%dT%H:%M:%S")
                self.signal_filter.minTs = self.signal_filter.minTs.strftime("%Y-%m-%dT%H:%M:%S")
            else:
                self.__to_ts()

    def __to_ts(self):
        try:
            min_ts = Timestamp(self.__signal_filter.minTs)
            max_ts = Timestamp(self.__signal_filter.maxTs)
            self.__check_date(min_ts, max_ts)
        except NapbotsReportingServiceValueError as ve:
            raise ve

    def __check_date(self, min_ts: Timestamp, max_ts: Timestamp):

        time_dela = max_ts - min_ts
        if max_ts < min_ts:
            raise NapbotsReportingServiceException("Max TimeStamp should be after Min TimeStamp")
        if len(self.__signal_filter.productCodes) == 1 and time_dela.days < 30:
            pass
