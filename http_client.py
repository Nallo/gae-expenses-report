from abc import ABC, abstractmethod
from http_response import HTTPResponse


class HTTPClient(ABC):
    @abstractmethod
    def get(self, url, query_params: dict = {}) -> HTTPResponse:
        ...