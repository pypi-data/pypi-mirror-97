__author__ = "hugo.inzirillo"

from dataclasses import dataclass


@dataclass
class EodQuotePk:
    productCode: str = None
    date: str = None

    def __hash__(self):
        return hash((self.productCode, self.date))

    def __eq__(self, other):
        return self.productCode == other.productCode and self.date == other.date \
            if isinstance(other, self.__class__) else False

    def __le__(self, other):
        return self.date <= other.date

    def __ge__(self, other):
        return self.date >= other.date

    def __lt__(self, other):
        return self.date < other.date

    def __gt__(self, other):
        return self.date > other.date


@dataclass
class EodQuote:
    pk: EodQuotePk = None
    open: float = None
    close: float = None
    low: float = None
    high: float = None
    totalReturnClose: float = None
    volume: float = None
    marketCap: float = None
    adjMarketCap: float = None
    adjClose: float = None
    divisor: float = None

    def __hash__(self):
        return hash(self.pk)

    def __eq__(self, other):
        return self.pk == other.pk if isinstance(other, self.__class__) else False

    def from_dict(self, dict_object: dict):
        if isinstance(dict_object, dict):
            self.pk = EodQuotePk(productCode=dict_object["productCode"],
                                 date=dict_object["date"])

            self.close = dict_object["close"]
            self.totalReturnClose = dict_object["totalReturnClose"]
            return self

    def __le__(self, other):
        return self.pk <= other.pk

    def __ge__(self, other):
        return self.pk >= other.pk

    def __lt__(self, other):
        return self.pk < other.pk

    def __gt__(self, other):
        return self.pk > other.pk