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
            raise GCalService.ClientException(e)

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
        exception_description = "some exception description"
        client, sut = self._make_sut()
        client.mock_failure(Exception(exception_description))

        self._assert_sut_raises_exception(
            sut=sut,
            expected_e_type=GCalService.ClientException,
            expected_e_msg=exception_description
        )

    def test_get_events_throws_invalid_data_exception_on_non_200_http_response(self) -> None:
        invalid_status_codes = [201, 300, 400, 500]
        client, sut = self._make_sut()

        for invalid_status_code in invalid_status_codes:
            client.mock_response(status_code=invalid_status_code)

            self._assert_sut_raises_exception(
                sut=sut,
                expected_e_type=GCalService.InvalidData,
                expected_e_msg="client completed with {} status code".format(invalid_status_code)
            )

    # Helpers

    def _make_sut(self, base_url: str = "http://any-url.com") -> tuple[HTTPClientSpy, GCalService]:
        client = HTTPClientSpy()
        sut = GCalService(base_url=base_url, client=client)

        return (client, sut)

    def _date_one_giant_leap_for_mankind(self) -> tuple[datetime.date, str]:
        date = datetime.datetime(year=1969, month=7, day=20, hour=22, minute=56, tzinfo=datetime.timezone.utc)
        date_str = "1969-07-20T22:56:00+00:00"
        return date, date_str
    
    def _assert_sut_raises_exception(self, sut: GCalService, expected_e_type: Exception, expected_e_msg: str) -> None:
        any_calendar_id = "my-calendar-id"
        any_date, _ = self._date_one_giant_leap_for_mankind()
        
        try:
            sut.get_events(calendar_id=any_calendar_id, from_date=any_date, until_date=any_date)
        except Exception as received_e:
            assert type(received_e) == expected_e_type, "Expected '{}' got '{}' instead".format(expected_e_type, type(received_e))
            assert str(received_e) == expected_e_msg, "Expected exception message '{}'. Got '{}' instead".format(expected_e_msg, str(received_e))