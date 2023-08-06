__author__ = "hugo.inzirillo"

from dataclasses import dataclass


@dataclass(frozen=False)
class PortfolioDecomposition:
    ts: str
    underlying: str
    weight: float
    quantity: float
    close: float
    usd_amount:float=None
    def __post_init__(self):
        self.usd_amount = self.quantity * self.close

    def __eq__(self, other):
        return self.underlying == other.underlying and self.ts == other.ts if isinstance(other,
                                                                                         self.__class__) else False

    def __ne__(self, other):
        return self.underlying != other.underlying and self.ts != other.ts if isinstance(other,
                                                                                         self.__class__) else True

    def __le__(self, other):
        return self.ts <= other.ts

    def __ge__(self, other):
        return self.ts >= other.ts

    def __lt__(self, other):
        return self.ts < other.ts

    def __gt__(self, other):
        return self.ts > other.ts
