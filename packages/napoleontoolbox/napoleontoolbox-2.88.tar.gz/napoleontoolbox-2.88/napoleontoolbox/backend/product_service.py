__author__ = "hugo.inzirillo"

from typing import Iterator, Set, Dict

from bifrost import NapoleonProductServiceConnector

from napoleontoolbox. models.product import Product
from napoleontoolbox. models.strats import __MAPPING__


class NapoleonProductService(object):
    def __init__(self):
        self.__product_connector = NapoleonProductServiceConnector()

    @property
    def product_connector(self):
        return self.__product_connector

    def get_all(self) -> Iterator[Product]:
        return iter(Product().from_dict(item) for item in self.product_connector.get_all())

    def get(self, product_code: str) -> Product:
        # todo : modifier bifrost pour avoir la compatibilité des types
        return Product().from_dict(self.product_connector.get(product_code=product_code))

    def get_products(self, product_codes: str) -> Product:
        try:
            return self.get(product_code=product_codes)
        except Exception as e:
            raise e

    def __get_product_all_by_product_code(self) -> Dict[str, Product]:
        all_products = self.get_all()
        return {product.productCode: product for product in all_products}

    def get_registered_strategies(self) -> Set[Product]:
        try:
            all_products = self.__get_product_all_by_product_code()
            return {all_products.get(item) for item in map(lambda x: x.value, __MAPPING__.values())}
        except Exception as e:
            raise
