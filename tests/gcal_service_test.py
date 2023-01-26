from tests.utils.http_client_spy import HTTPClientSpy

class GCalService:
    pass

class Test_GCalService:
    def test_init_does_not_request_data_from_url(self) -> None:
        client = HTTPClientSpy()
        _ = GCalService()

        assert client.requested_urls == []