from tests.utils.http_client_spy import HTTPClientSpy

class GCalService:
    def __init__(self, base_url) -> None:
        pass

class Test_GCalService:
    def test_init_does_not_request_data_from_url(self) -> None:
        any_url = "http://any-url.com"
        client = HTTPClientSpy()
        _ = GCalService(base_url=any_url)

        assert client.requested_urls == []