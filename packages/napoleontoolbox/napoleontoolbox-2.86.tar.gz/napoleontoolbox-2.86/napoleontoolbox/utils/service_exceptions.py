__author__ = "hugo.inzirillo"

from dataclasses import dataclass
from enum import Enum


class NapbotsReportingServiceException(Exception):
    pass


class NapbotsReportingServiceValueError(ValueError):
    pass


class Error(Enum):
    InvalidTs = 0


@dataclass(init=True)
class PositionReportingServiceError:
    error: str
    code: int
