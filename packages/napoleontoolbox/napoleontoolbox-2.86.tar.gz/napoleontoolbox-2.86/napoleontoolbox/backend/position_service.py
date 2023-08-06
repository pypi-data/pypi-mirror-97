__author__ = "hugo.inzirillo"

from typing import List

from bifrost import NapoleonPositionServiceConnector

from napoleontoolbox.models.filter import SignalComputationFilter


class NapoleonPositionService(object):
    def __init__(self):
        self.__position_connector = NapoleonPositionServiceConnector()

    @property
    def position_connector(self):
        return self.__position_connector

    def filter(self, filter: SignalComputationFilter) -> List[dict]:
        return self.position_connector.filter(data=filter)



if __name__ == '__main__':
    a = NapoleonPositionService()
