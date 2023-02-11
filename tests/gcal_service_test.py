import datetime
import pytest
from tests.utils.http_client_spy import HTTPClientSpy


class GCalService:
    def __init__(self, base_url: str, client: HTTPClientSpy) -> None:
        self._base_url = base_url
        self._client = client

    def get_events(self, calendar_id: str, until_date: datetime.date, from_date: datetime.date) -> None:
        url = self._base_url
        url += "/calendars/"
        url += calendar_id
        url += "/events"

        query_params = {
            "orderBy": "startTime",
            "q": "💸",
            "singleEvents": True,
            "timeMax": until_date.isoformat(),
            "timeMin": from_date.isoformat(),
        }

        try:
            response = self._client.get(url=url, query_params=query_params)
        except Exception as e:
            raise GCalService.ClientException(e.args)

        if response and response.status_code != 200:
            raise GCalService.InvalidData("client completed with {} status code".format(response.status_code))

    class ClientException(Exception):
        pass

    class InvalidData(Exception):
        pass


class Test_GCalService:
    def test_init_does_not_request_data_from_url(self) -> None:
        client, _ = self._make_sut()

        assert client.requested_urls == []

    def test_get_events_requests_data_from_url(self) -> None:
        a_url = "http://my-url.com"
        a_calendar_id = "my-calendar-id"
        a_date, _ = self._date_one_giant_leap_for_mankind()
        client, sut = self._make_sut(base_url=a_url)

        sut.get_events(calendar_id=a_calendar_id, from_date=a_date, until_date=a_date)

        assert client.requested_urls == [a_url + "/calendars/" + a_calendar_id + "/events"]

    def test_get_events_sets_correct_query_parameters(self) -> None:
        a_calendar_id = "my-calendar-id"
        a_date, a_date_str = self._date_one_giant_leap_for_mankind()
        client, sut = self._make_sut()

        sut.get_events(
            calendar_id=a_calendar_id, 
            from_date=a_date,
            until_date=a_date,
        )

        assert client.requested_query_parameter(key="orderBy", value="startTime")
        assert client.requested_query_parameter(key="q", value="💸")
        assert client.requested_query_parameter(key="singleEvents", value=True)
        assert client.requested_query_parameter(key="timeMax", value=a_date_str)
        assert client.requested_query_parameter(key="timeMin", value=a_date_str)

    def test_get_events_throws_client_exception_when_client_throws_any_exception(self) -> None:
        a_calendar_id = "my-calendar-id"
        a_date, _ = self._date_one_giant_leap_for_mankind()
        client, sut = self._make_sut()
        exception_description = "some expection description"
        client.mock_failure(Exception(exception_description))

        with pytest.raises(GCalService.ClientException, match=exception_description):
            sut.get_events(calendar_id=a_calendar_id, from_date=a_date, until_date=a_date)

    def test_get_events_throws_invalid_data_exception_on_non_200_http_response(self) -> None:
        a_calendar_id = "my-calendar-id"
        a_date, _ = self._date_one_giant_leap_for_mankind()
        invalid_status_code = 500
        client, sut = self._make_sut()
        client.mock_response(status_code=invalid_status_code)

        with pytest.raises(GCalService.InvalidData, match="client completed with {} status code".format(invalid_status_code)):
            sut.get_events(calendar_id=a_calendar_id, from_date=a_date, until_date=a_date)

    # Helpers

    def _make_sut(self, base_url: str = "http://any-url.com") -> tuple[HTTPClientSpy, GCalService]:
        client = HTTPClientSpy()
        sut = GCalService(base_url=base_url, client=client)

        return (client, sut)

    def _date_one_giant_leap_for_mankind(self) -> tuple[datetime.date, str]:
        date = datetime.datetime(year=1969, month=7, day=20, hour=22, minute=56, tzinfo=datetime.timezone.utc)
        date_str = "1969-07-20T22:56:00+00:00"
        return date, date_str
