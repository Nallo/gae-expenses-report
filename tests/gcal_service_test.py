from tests.utils.http_client_spy import HTTPClientSpy


class GCalService:
    def __init__(self, base_url: str, client: HTTPClientSpy) -> None:
        self._base_url = base_url
        self._client = client

    def get_events(self, calendar_id: str) -> None:
        url = self._base_url
        url += "/calendars/"
        url += calendar_id
        url += "/events"

        self._client.get(url=url)


class Test_GCalService:
    def test_init_does_not_request_data_from_url(self) -> None:
        client, _ = self._make_sut()

        assert client.requested_urls == []

    def test_get_events_requests_data_from_url(self) -> None:
        a_url = "http://my-url.com"
        a_calendar_id = "my-calendar-id"
        client, sut = self._make_sut(base_url=a_url)

        sut.get_events(calendar_id=a_calendar_id)

        assert client.requested_urls == [a_url + "/calendars/" + a_calendar_id + "/events"]

    # Helpers

    def _make_sut(self, base_url: str = "http://any-url.com") -> tuple[HTTPClientSpy, GCalService]:
        client = HTTPClientSpy()
        sut = GCalService(base_url=base_url, client=client)

        return (client, sut)
