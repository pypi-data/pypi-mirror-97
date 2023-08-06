__author__ = "hugo.inzirillo"

from enum import Enum


class StratType(Enum):
    BLEND = "BLEND"
    BENCH = "BENCH"
    CRON_STRAT = "CRON_STRAT"
    AT_CLOSE_STRAT = "AT_CLOSE_STRAT"
    PROTECTED = "PROTECTED"


class StratTypeView(Enum):
    BLEND = "BLEND"
    BENCH = "BENCH"
    CRON_STRAT = "HOURLY"
    AT_CLOSE_STRAT = "DAILY"


class StratNapBotsCode(Enum):
    STRAT_BTC_ETH_USD_H_1 = "STRAT_BTC_ETH_USD_H_1"
    STRAT_ETH_USD_FUNDING_8H_1 = "STRAT_ETH_USD_FUNDING_8H_1"
    STRAT_ETH_USD_H_4 = "STRAT_ETH_USD_H_4"
    STRAT_BTC_USD_H_4 = "STRAT_BTC_USD_H_4"
    STRAT_BTC_USD_FUNDING_8H_1 = "STRAT_BTC_USD_FUNDING_8H_1"
    STRAT_BTC_USD_H_3_V2 = "STRAT_BTC_USD_H_3_V2"
    STRAT_BTC_ETH_USD_LO_H_1 = "STRAT_BTC_ETH_USD_LO_H_1"
    STRAT_ETH_USD_H_3_V2 = "STRAT_ETH_USD_H_3_V2"
    STRAT_ETH_USD_VOLUME_H_1 = "STRAT_ETH_USD_VOLUME_H_1"
    STRAT_BTC_ETH_USD_D_1 = "STRAT_BTC_ETH_USD_D_1"
    STRAT_ETH_USD_2 = "STRAT_ETH_USD_2"
    STRAT_BNB_USD_LO_D_1 = "STRAT_BNB_USD_LO_D_1"
    STRAT_BTC_USD_VOLUME_H_1 = "STRAT_BTC_USD_VOLUME_H_1"
    STRAT_BTC_USD_D_2 = "STRAT_BTC_USD_D_2"
    STRAT_BCH_USD_LO_D_1 = "STRAT_BCH_USD_LO_D_1"
    STRAT_BTC_ETH_USD_LO_D_1 = "STRAT_BTC_ETH_USD_LO_D_1"
    STRAT_ETH_USD_D_3 = "STRAT_ETH_USD_D_3"
    STRAT_BTC_USD_D_3 = "STRAT_BTC_USD_D_3"
    STRAT_EOS_USD_D_2 = "STRAT_EOS_USD_D_2"
    STRAT_LTC_USD_D_1 = "STRAT_LTC_USD_D_1"
    STRAT_XRP_USD_D_1 = "STRAT_XRP_USD_D_1"


__MAPPING__ = {"NapoX ETH/BTC/USD Hourly": StratNapBotsCode.STRAT_BTC_ETH_USD_H_1,
               "NapoX ETH Funding AR": StratNapBotsCode.STRAT_ETH_USD_FUNDING_8H_1,
               "NapoX ETH Hourly 1": StratNapBotsCode.STRAT_ETH_USD_H_4,
               "NapoX BTC Hourly 1": StratNapBotsCode.STRAT_BTC_USD_H_4,
               "NapoX BTC Funding AR": StratNapBotsCode.STRAT_BTC_USD_FUNDING_8H_1,
               "NapoX BTC Hourly 2": StratNapBotsCode.STRAT_BTC_USD_H_3_V2,
               "NapoX ETH/BTC/USD LO Hourly": StratNapBotsCode.STRAT_BTC_ETH_USD_LO_H_1,
               "NapoX ETH Hourly 2": StratNapBotsCode.STRAT_ETH_USD_H_3_V2,
               "NapoX ETH Volume AR": StratNapBotsCode.STRAT_ETH_USD_VOLUME_H_1,
               "NapoX ETH/BTC/USD AR": StratNapBotsCode.STRAT_BTC_ETH_USD_D_1,
               "NapoX ETH AR": StratNapBotsCode.STRAT_ETH_USD_2,
               "NapoX BNB LO": StratNapBotsCode.STRAT_BNB_USD_LO_D_1,
               "NapoX BTC Volume AR": StratNapBotsCode.STRAT_BTC_USD_VOLUME_H_1,
               "NapoX BTC AR": StratNapBotsCode.STRAT_BTC_USD_D_2,
               "NapoX BCH LO": StratNapBotsCode.STRAT_BCH_USD_LO_D_1,
               "NapoX ETH/BTC/USD LO": StratNapBotsCode.STRAT_BTC_ETH_USD_LO_D_1,
               "NapoX ETH LO": StratNapBotsCode.STRAT_ETH_USD_D_3,
               "NapoX BTC LO": StratNapBotsCode.STRAT_BTC_USD_D_3,
               "NapoX EOS LO": StratNapBotsCode.STRAT_EOS_USD_D_2,
               "NapoX LTC LO": StratNapBotsCode.STRAT_LTC_USD_D_1,
               "NapoX XRP LO": StratNapBotsCode.STRAT_XRP_USD_D_1}
