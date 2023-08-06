__author__ = "hugo.inzirillo"

from dataclasses import dataclass
from typing import List, Union
from datetime import time
from pandas import Timestamp, Timedelta
from itertools import product

@dataclass
class Product:
    productCode: str = None
    label: str = None
    currency: str = None
    productType: str = None
    stratType: str = None
    basketProfile: str = None
    basketReturnType: str = None
    rebalancingPeriod: str = None
    inceptionDate: str = None
    initialValue: float = None
    underlyings: List[str] = None
    market: str = None
    creationTs: str = None
    groups: List[str] = None
    maturity: str = None
    isFrontFuture: bool = None
    futurePeriodicity: str = None
    underlyingFuture: str = None
    rollNDaysBeforeMaturity: int = None
    targetVol: float = None
    guaranteedRate: float = None
    maxLeverage: float = None
    numberOfDecimalsForCalculation: int = None
    numberOfDecimalsForDisplay: str = None
    stratCron: str = None
    expired: bool = None

    def from_dict(self, dict_object: dict):
        if isinstance(dict_object, dict):
            self.__dict__ = dict_object
            return self

    def __repr__(self):
        return self.productCode

    def __hash__(self):
        return hash(self.productCode) if self.productCode is not None else 0

    def __eq__(self, other):
        return self.productCode == other.productCode if isinstance(other,
                                                                   self.__class__) else False


@dataclass
class ProductView:
    productCode: str = None
    label: str = None
    stratType: str = None
    underlyings: List[str] = None

    def from_dict(self, dict_object: dict):
        if isinstance(dict_object, dict):
            self.__dict__ = {key: value for key, value in dict_object.items()
                             if key in set(dict_object.keys()).intersection(set(self.__dict__.keys()))}
            return self

    def __repr__(self):
        return self.productCode

    def __hash__(self):
        return hash(self.productCode) if self.productCode is not None else 0


@dataclass
class EodQuoteProductCodeBuilder:
    underlying: str
    date: [Union[str, Timestamp, Timedelta]]
    product_code: str = None

    def __post_init__(self):
        if self.product_code is None and isinstance(self.date, str):
            self.product_code = self.underlying + "-" + str(Timestamp(self.date).hour) + "H"
        if self.product_code is None and isinstance(self.date, Timestamp):
            self.product_code = self.underlying + "-" + str(self.date.hour) + "H"
        if self.product_code is None and isinstance(self.date, time):
            self.product_code = self.underlying + "-" + str(self.date.hour) + "H"


    @staticmethod
    def product_code_generator(udl_code: List[str]):
        product_code_combination = product(udl_code, range(0, 24))
        return [EodQuoteProductCodeBuilder(product_code, time(hour=hour)).product_code for product_code, hour in
                product_code_combination]


    def __hash__(self):
        return hash(self.product_code)

    def __eq__(self, other):
        return self.product_code == other if isinstance(other, self.__class__) else False


if __name__ == '__main__':
    test = ProductView().from_dict(Product(productCode="Hello", label="Test", stratType=",elf,ezof,zeof,zef").__dict__)
    # ProductView(productCode=prod.productCode, label=prod.label, stratType=prod.stratType, underlyings=prod.underlyings)
