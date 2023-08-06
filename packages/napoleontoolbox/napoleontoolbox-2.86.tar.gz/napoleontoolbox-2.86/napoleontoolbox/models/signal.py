__author__ = "hugo.inzirillo"

from dataclasses import dataclass

from pandas import Timestamp, Timedelta

from napoleontoolbox.models.strats import StratType


@dataclass
class SignalComputationPk:
    productCode: str
    underlyingCode: str
    ts: str

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
class SignalComputation:
    """
    Position Service
    Mapping of Java Objects
    """
    pk: SignalComputationPk = None
    value: float = None

    def from_dict(self, dict_object: dict, strat_type: StratType = None):
        if strat_type:
            if strat_type.value == StratType.AT_CLOSE_STRAT.value:
                dict_object["ts"] = (Timestamp(dict_object["ts"]) + Timedelta(hours=1)).strftime("%Y-%m-%dT%H:00:00")
            elif strat_type == StratType.CRON_STRAT:
                if strat_type.value == StratType.AT_CLOSE_STRAT.value:
                    dict_object["ts"] = Timestamp(dict_object["ts"]).strftime("%Y-%m-%dT%H:00:00")
        else:
            dict_object["ts"] = Timestamp(dict_object["ts"]).strftime("%Y-%m-%dT%H:00:00")

        self.pk = SignalComputationPk(dict_object["productCode"], dict_object["underlyingCode"], dict_object["ts"])
        self.value = dict_object["value"]
        return self

    def __hash__(self):
        return hash((self.pk))

    def __eq__(self, other):
        return self.pk == other.pk if isinstance(other, self.__class__) else False


@dataclass
class SignalComputationView:
    productCode: str = None
    underlyingCode: str = None
    ts: str = None
    value: float = None
