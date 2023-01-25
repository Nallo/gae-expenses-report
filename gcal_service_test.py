class GCalService:
    pass

class HTTPClientSpy:
    def __init__(self):
        self.requested_urls = []


class Test_GCalService:
    def test_init_does_not_request_data_from_url(self):
        client = HTTPClientSpy()
        _ = GCalService()

        assert client.requested_urls == []