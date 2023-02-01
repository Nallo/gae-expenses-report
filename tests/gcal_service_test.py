import datetime
import pytest
from tests.utils.http_client_spy import HTTPClientSpy


class GCalService:
    def __init__(self, base_url: str, client: HTTPClientSpy) -> None:
        self._base_url = base_url
        self._client = client

    def get_events(self, calendar_id: str, until_date: datetime.date, lower_bound_ts: str = "") -> None:
        url = self._base_url
        url += "/calendars/"
        url += calendar_id
        url += "/events"

        query_params = {
            "orderBy": "startTime",
            "q": "💸",
            "singleEvents": True,
            "timeMax": until_date,
            "timeMin": lower_bound_ts,
        }

        try:
            self._client.get(url=url, query_params=query_params)
        except Exception as e:
            raise GCalService.ClientException(e.args)

    class ClientException(Exception):
        pass


class Test_GCalService:
    def test_init_does_not_request_data_from_url(self) -> None:
        client, _ = self._make_sut()

        assert client.requested_urls == []

    def test_get_events_requests_data_from_url(self) -> None:
        a_url = "http://my-url.com"
        a_calendar_id = "my-calendar-id"
        client, sut = self._make_sut(base_url=a_url)

        sut.get_events(calendar_id=a_calendar_id, until_date=self._any_date())

        assert client.requested_urls == [a_url + "/calendars/" + a_calendar_id + "/events"]

    def test_get_events_sets_correct_query_parameters(self) -> None:
        a_calendar_id = "my-calendar-id"
        a_time = "some time"
        another_time = "some other time"
        client, sut = self._make_sut()

        sut.get_events(
            calendar_id=a_calendar_id, 
            until_date=a_time,
            lower_bound_ts=another_time,
        )

        assert client.requested_query_parameter(key="orderBy", value="startTime")
        assert client.requested_query_parameter(key="q", value="💸")
        assert client.requested_query_parameter(key="singleEvents", value=True)
        assert client.requested_query_parameter(key="timeMax", value=a_time)
        assert client.requested_query_parameter(key="timeMin", value=another_time)

    def test_get_events_throws_client_excpetion_when_client_throws_any_exception(self) -> None:
        a_calendar_id = "my-calendar-id"
        client, sut = self._make_sut()
        exception_description = "some expection description"
        client._mocked_error = Exception(exception_description)

        with pytest.raises(GCalService.ClientException, match=exception_description):
            sut.get_events(calendar_id=a_calendar_id, until_date=self._any_date())

    # Helpers

    def _make_sut(self, base_url: str = "http://any-url.com") -> tuple[HTTPClientSpy, GCalService]:
        client = HTTPClientSpy()
        sut = GCalService(base_url=base_url, client=client)

        return (client, sut)

    def _any_date(self) -> datetime.date:
        return datetime.datetime.now()
