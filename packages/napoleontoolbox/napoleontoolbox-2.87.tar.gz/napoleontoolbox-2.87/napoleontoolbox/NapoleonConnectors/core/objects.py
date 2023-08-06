__author__ = "hugo.inzirillo"

from abc import abstractmethod, ABCMeta
from typing import Union

from napoleontoolbox.bifrost import ClientCredentials, PasswordCredentials, Token


class AbstractHeadersTemplate(metaclass=ABCMeta):

    @property
    @abstractmethod
    def value(self):
        raise NotImplemented

    @staticmethod
    def build(object: Union[PasswordCredentials, ClientCredentials, Token]):
        raise NotImplemented


class AbstractHeaders(AbstractHeadersTemplate):

    @property
    @abstractmethod
    def value(self):
        raise NotImplemented

    @staticmethod
    def build(object: Union[PasswordCredentials, ClientCredentials, Token]):
        raise NotImplemented


class AbstractHeadersScheme(AbstractHeadersTemplate):

    @property
    @abstractmethod
    def value(self):
        raise NotImplemented

    @staticmethod
    def build(object: Union[PasswordCredentials, ClientCredentials, Token]):
        raise NotImplemented


class HeadersScheme(AbstractHeadersTemplate):

    def __init__(self):
        self.__value = None

    def value(self):
        pass

    @staticmethod
    def build(object: Union[PasswordCredentials, ClientCredentials, Token]):
        pass


class TemplateHeaders(AbstractHeaders):

    def value(self): ...

    @staticmethod
    def build(object: Union[PasswordCredentials, ClientCredentials, Token]): ...


class Headers(TemplateHeaders):
    def __init__(self):
        self.__content = None
        self.__value = dict()

    @property
    def value(self) -> dict:
        return self.__value

    def __dict__(self):
        return self.__value

    @staticmethod
    def build(o: Union[PasswordCredentials, ClientCredentials, Token]):
        return HeaderGenerator().build(o).value


class AuthenticationHeader(TemplateHeaders):
    pass


class HeaderGenerator(AbstractHeaders):
    def __init__(self):
        self.__header = None

    @property
    def value(self):
        return self.__header

    def build(self, object: Union[PasswordCredentials, ClientCredentials, Token]):
        if isinstance(self.__header.content, ClientCredentials):
            return None
        elif isinstance(self.__header.content, PasswordCredentials):
            return None
        elif isinstance(self.__header.content, Token):
            return None
        return self
