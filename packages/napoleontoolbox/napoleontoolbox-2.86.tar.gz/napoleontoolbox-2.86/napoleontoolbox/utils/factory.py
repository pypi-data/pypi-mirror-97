__author__ = "hugo.inzirillo"

from collections import OrderedDict
from itertools import groupby
from typing import List, Set, Dict, Callable

from pandas import DataFrame, Timestamp

from napoleontoolbox.models.filter import SignalComputationFilter
from napoleontoolbox.models.portfolio import Portfolio, PortfolioPk, PortfolioView
from napoleontoolbox.models.portfolio_decomposition import PortfolioDecomposition
from napoleontoolbox.models.product import Product, ProductView, EodQuoteProductCodeBuilder
from napoleontoolbox.models.quantity import Quantity
from napoleontoolbox.models.quote import EodQuotePk, EodQuote
from napoleontoolbox.models.request_portfolio_analysis import RequestPortfolioAnalysis
from napoleontoolbox.models.signal import SignalComputation, SignalComputationView
from napoleontoolbox.models.strats import StratTypeView


class SignalComputationFilterFactory(object):

    def to_signal_filer(self, product_codes: List[str], min_ts=None, max_ts=None, last_only: bool = True):
        return SignalComputationFilter(productCodes=product_codes, minTs=min_ts, maxTs=max_ts, lastOnly=last_only)

    def to_dict(self, signal_filter: SignalComputationFilter):
        return signal_filter.__dict__


class EodQuotePkFactory(object):
    def to_ts(self, pk: EodQuotePk):
        return Timestamp(pk.date + "T" + "{hour}:00:00".format(hour=pk.productCode.split("-")[2][:-1]))


class EodQuoteFactory(object):
    def groupby(self, iterable: List[EodQuote], key: Callable[[EodQuote], str]):
        return {pk: list(_grouper) for pk, _grouper in
                groupby(sorted(iterable, key=key, reverse=True), key)}


    def to_ordered_dict(self,quotes:List[EodQuote]):
        return OrderedDict({EodQuotePkFactory().to_ts(pk): quote[0].close for pk, quote in
                                             EodQuoteFactory().groupby(quotes, lambda quote: quote.pk).items()})


class ProductFactory(object):

    def __from_set_to_dict(self, product_set: Set[Product]) -> Dict[str, Product]:
        return {item.productCode: item.__dict__ for item in product_set}

    def to_df(self, product_set: Set[Product]):
        return DataFrame.from_dict(data=self.__from_set_to_dict(product_set), orient="index")

    def groupby(self, iterable: Set[Product], key: Callable[[Product], str]):
        return {strat_type: set(_grouper) for strat_type, _grouper in
                groupby(sorted(iterable, key=key, reverse=True), key)}

    def to_view(self, product: Product):
        product_view = ProductView()
        product_view.stratType = StratTypeView.__getitem__(product.stratType).value
        product_view.label = product.label
        product_view.underlyings = product.underlyings
        product_view.productCode = product.productCode
        return product_view

    def to_product(self, product_view: ProductView):
        product = Product()
        product.productCode = None
        product.label = product_view.label
        product.stratType = product_view.stratType
        product.underlyings = product_view.underlyings
        return product


class SignalComputationFactory(object):
    def groupby(self, iterable: List[SignalComputation]
                , key: Callable[[SignalComputation], str]) -> Dict[str, List[SignalComputation]]:
        return {strat_type: set(_grouper) for strat_type, _grouper in
                groupby(sorted(iterable, key=key, reverse=True), key)}

    def to_view(self, signal: SignalComputation) -> SignalComputationView:
        return SignalComputationView(signal.pk.productCode, signal.pk.underlyingCode, signal.pk.ts, signal.value)


class QuantityFactory(object):
    def to_view(self, quantity: Quantity) -> SignalComputationView:
        return SignalComputationView(quantity.pk.productCode, quantity.pk.underlyingCode, quantity.pk.ts,
                                     quantity.value)


class RequestPortfolioAnalysisFactory(object):
    def to_portfolio(self, request: RequestPortfolioAnalysis) -> Portfolio:
        pk = PortfolioPk(request.amount, request.leverage, request.composition, request.start_date, request.end_date)
        portfolio = Portfolio(pk=pk, products=request.products)
        return portfolio


class PortfolioFactory(object):
    TS = "ts"
    UDL_CODE = "underlyingCode"
    VALUE = "value"

    def to_view(self, portfolio: Portfolio):
        return PortfolioView().from_dict(portfolio.__dict__)

    def to_portfolio_decomposition(self, porfolio: Portfolio, quotes: Dict[EodQuotePk, EodQuote]) -> List[
        PortfolioDecomposition]:
        res = list()
        agg_weights_by_ts = self.__get_aggregated_weight_values(porfolio.positions)
        agg_quantities_by_ts = self.__get_aggregated_quantity_values(porfolio.quantities)
        ts_udl = set(agg_quantities_by_ts.keys())
        for ts, udl in ts_udl:
            res.append(
                PortfolioDecomposition(ts, udl, agg_weights_by_ts.get((ts, udl)), agg_quantities_by_ts.get((ts, udl)),
                                       quotes.get(
                                           EodQuotePk(EodQuoteProductCodeBuilder(udl, self.to_date(ts)).product_code,
                                                      self.to_date(ts))).close
                                       )
            )

        return res

    def __get_aggregated_quantity_values(self, quantity_list: List[Quantity]) -> Dict:
        quantity_list = [QuantityFactory().to_view(quantity) for quantity in quantity_list]
        df = DataFrame(quantity_list)
        return \
            df.groupby([PortfolioFactory.TS, PortfolioFactory.UDL_CODE])[[PortfolioFactory.VALUE]].sum().to_dict()[
                PortfolioFactory.VALUE]

    def __get_aggregated_weight_values(self, signal_list: List[SignalComputation]) -> Dict:
        weight_list = [SignalComputationFactory().to_view(signal) for signal in signal_list]
        df = DataFrame(weight_list)
        return \
            df.groupby([PortfolioFactory.TS, PortfolioFactory.UDL_CODE])[[PortfolioFactory.VALUE]].sum().to_dict()[
                PortfolioFactory.VALUE]

    def to_date(self, ts: str) -> str:
        return Timestamp(ts).strftime("%Y-%m-%d")
