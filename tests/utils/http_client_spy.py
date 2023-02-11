from typing import Any
import pytest

class HTTPResponse:
    def __init__(self, status_code: int, body: str) -> None:
        self.status_code = status_code
        self.body = body


class HTTPClientSpy:
    def __init__(self) -> None:
        self.requested_urls = []
        self._requested_query_params = {}
        self._mocked_error = None
        self._mocked_response = None

    def get(self, url, query_params: dict = {}) -> HTTPResponse:
        self.requested_urls.append(url)
        self._requested_query_params = query_params

        if self._mocked_error:
            raise self._mocked_error
        else:
            return self._mocked_response

    def requested_query_parameter(self, key: str, value: Any) -> bool:
        if key not in self._requested_query_params:
            pytest.fail("key {} not found in requested query parameters".format(key))
        elif self._requested_query_params[key] != value:
            expected_value = value
            received_value = self._requested_query_params[key]
            pytest.fail("expected value {} for key {}, got {} instead".format(expected_value, key, received_value))
        else:
            return True

    def mock_failure(self, e: Exception) -> None:
        self._mocked_error = e

    def mock_response(self, status_code: int, body: str = '') -> None:
        self._mocked_response = HTTPResponse(status_code=status_code, body=body)
