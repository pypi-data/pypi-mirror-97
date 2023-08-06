__author__ = "hugo.inzirillo"

import logging
import sys
from abc import ABCMeta, abstractmethod

__version__ = "0.0.1"


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances.keys():
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class AbstractLoggerManager(metaclass=ABCMeta):

    @abstractmethod
    def get_logger(self, name=None):
        """

        Parameters
        ----------
        name : current name of the npxlogger

        Returns
        -------

        """
        return NapoleonLoggerManager._loggers[name]

    @property
    @abstractmethod
    def basic_config(self):
        """

        Returns
        -------

        """
        raise NotImplemented

    @property
    @abstractmethod
    def config(self) -> dict:
        """

        Returns
        -------

        """
        raise NotImplemented

    @property
    @abstractmethod
    def handler(self):
        """

        Returns
        -------

        """
        raise NotImplemented

    @property
    @abstractmethod
    def log_level(self):
        """

        Returns
        -------

        """
        raise NotImplemented

    @property
    @abstractmethod
    def handler_level(self):
        """

        Returns
        -------

        """
        raise NotImplemented


class _LoggerManager(AbstractLoggerManager):

    @property
    def log_level(self):
        return logging.DEBUG

    @property
    def handler_level(self):
        return logging.NOTSET

    @property
    def handler(self) -> logging.StreamHandler:
        console = logging.StreamHandler(stream=sys.stdout)
        console.setLevel(self.handler_level)
        console.setFormatter(logging.Formatter(self.get_format()))
        return console

    def get_logger(self, name=None):
        """

        Parameters
        ----------
        name : current name of the npxlogger

        Returns
        -------

        """
        if name is None:
            logging.basicConfig()
            return logging.getLogger()

    @property
    def basic_config(self):
        """

        Returns
        -------

        """
        logging.basicConfig()
        raise logging.getLogger()

    @property
    def config(self) -> dict:
        """

        Returns
        -------

        """
        return dict(filename="napoleontoolbox.log",
                    format=self.get_format(),
                    level=self.log_level)

    def get_format(self):
        return "%(levelname) -10s %(asctime)s | module : %(module)s | line : %(lineno)s | method : %(funcName)s | %(message)s"


class _NapoleonLoggerManager(_LoggerManager):
    __metaclass__ = Singleton

    _loggers = {}

    def __init__(self, *args, **kwargs):
        super(_NapoleonLoggerManager, self).__init__()
        self.__config = None
        pass

    def get_logger(self, name=None) -> logging.Logger:
        """

        Parameters
        ----------
        name : current name of the npxlogger

        Returns
        -------

        """

        if name not in _NapoleonLoggerManager._loggers.keys():
            logging.basicConfig(**self.config)
            _NapoleonLoggerManager._loggers[name] = logging.getLogger(str(name))
            _NapoleonLoggerManager._loggers[name].addHandler(self.handler)
            return _NapoleonLoggerManager._loggers[name]

        elif not name:

            return super(_NapoleonLoggerManager, self).get_logger()


#NapoleonLoggerManager = _NapoleonLoggerManager
#log = _NapoleonLoggerManager().get_logger(__package__)
