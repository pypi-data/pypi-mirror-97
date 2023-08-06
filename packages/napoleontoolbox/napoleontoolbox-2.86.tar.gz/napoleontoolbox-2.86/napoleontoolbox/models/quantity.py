__author__ = "hugo.inzirillo"

from dataclasses import dataclass


@dataclass
class QuantityPk:
    productCode: str
    underlyingCode: str = None
    ts: str = None

    def __hash__(self):
        return hash((self.productCode, self.underlyingCode, self.ts))

    def __eq__(self, other):
        return self.productCode == other.productCode and self.underlyingCode == other.underlyingCode and \
               self.ts == other.ts if isinstance(other, self.__class__) else False

    def __ne__(self, other):
        return self.productCode != other.productCode and self.underlyingCode != other.underlyingCode and \
               self.ts != other.ts if isinstance(other, self.__class__) else True

    def __le__(self, other):
        return self.ts <= other.ts

    def __ge__(self, other):
        return self.ts >= other.ts

    def __lt__(self, other):
        return self.ts < other.ts

    def __gt__(self, other):
        return self.ts > other.ts


@dataclass
class Quantity:
    pk: QuantityPk = None
    value: float = None

    def __hash__(self):
        return hash(self.pk)

    def __eq__(self, other):
        return self.pk == other.pk if isinstance(other, self.__class__) else False

@dataclass
class QuantityView:
    productCode: str = None
    underlyingCode: str = None
    ts: str = None
    value: float = None
