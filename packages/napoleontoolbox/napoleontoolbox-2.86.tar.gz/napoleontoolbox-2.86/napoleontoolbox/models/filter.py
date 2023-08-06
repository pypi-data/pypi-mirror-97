__author__ = "hugo.inzirillo"

from dataclasses import dataclass
from typing import List, Dict

from pandas import Timestamp


@dataclass(frozen=False)
class SignalComputationFilter:
    """
    Position Service
    Mapping of Java Objects
    """
    productCodes: List[str]
    underlyingCodes: List[str] = None
    minTs: str = None
    maxTs: str = None
    lastOnly: bool = False

    def to_dict(self):
        return self.__dict__

    def __str__(self):
        return "SignalComputationFilter{productCodes=" + str(
            self.productCodes) + ", minTs=" + self.minTs + ", maxTs=" + self.maxTs + ", lastOnly=" + str(
            self.lastOnly) + '}'


@dataclass(frozen=True)
class EodQuoteFilter:
    """
    Product Service
    Mapping of Java Objects
    """
    productCodes: List[str]
    sources: List[str] =None
    minDate: str = None
    maxDate: str = None
    lastOnly: bool = False

    def to_dict(self):
        return self.__dict__

    def __str__(self):
        return "EodQuoteFilter{productCodes=" + str(
            self.productCodes) + ", minDate=" + self.minDate + ", maxDate=" + self.maxDate + ", lastOnly=" + str(
            self.lastOnly) + '}'


@dataclass(frozen=True)
class PortFolioFilter:
    compo: Dict[str, float]
    amount: float
    start_date: Timestamp
    end_date: Timestamp
