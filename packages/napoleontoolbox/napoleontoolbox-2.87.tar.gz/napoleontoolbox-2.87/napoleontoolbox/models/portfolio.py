__author__ = "hugo.inzirillo"

from dataclasses import dataclass
from typing import List, Dict

from pandas import Timestamp

from napoleontoolbox.models.product import Product
from napoleontoolbox.models.quantity import Quantity
from napoleontoolbox.models.signal import SignalComputation


@dataclass
class PortfolioPk:
    amount: float
    leverage: float
    composition: Dict[str, float]
    start_date: Timestamp
    end_date: Timestamp

    def __hash__(self):
        return hash((self.amount, self.leverage, self.composition, self.start_date, self.end_date))

    def __str__(self):
        return "PortfolioPk{amount=" + str(
            self.amount) + ", start_date=" + self.start_date + ", end_date=" + self.end_date + ", leverage=" + str(
            self.leverage) + '}'


@dataclass
class Portfolio:
    pk: PortfolioPk
    products: List[Product] = None
    positions: List[SignalComputation] = None
    quantities: List[Quantity] = None

    def __hash__(self):
        return hash((self.pk))

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.pk.__str__()

    def __eq__(self, other):
        return self.pk == other.pk if isinstance(other, self.__class__) else False


@dataclass
class PortfolioView:
    amount: float = None
    positions: List[SignalComputation] = None
    quantities: List[Quantity] = None

    def from_dict(self, dict_object: dict):
        if isinstance(dict_object, dict):
            self.__dict__ = {key: value for key, value in dict_object.items()
                             if key in set(dict_object.keys()).intersection(set(self.__dict__.keys()))}
            return self

    def __str__(self):
        return "Portfolio{amount=" + str(
            self.amount) + '}'


if __name__ == '__main__':
    pk = PortfolioPk(1000, 1.5, dict(STRAT_BTC_ETH_USD_LO_H_1=0.5, STRAT_BTC_ETH_USD_D_1=0.5), Timestamp.now(),
                     Timestamp.now())
    ptf = Portfolio(pk=pk)

    end = True
