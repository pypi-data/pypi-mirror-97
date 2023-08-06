__author__ = "hugo.inzirillo"

from dataclasses import dataclass
from typing import Dict, List

from pandas import Timestamp

from napoleontoolbox.models.product import Product


@dataclass
class RequestPortfolioAnalysis:
    amount: float
    leverage: float
    composition: Dict[str, float]
    start_date: Timestamp
    end_date: Timestamp
    products: List[Product]
