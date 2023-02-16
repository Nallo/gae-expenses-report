from collections import namedtuple
from datetime import datetime
import json
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

        if not response:
            raise GCalService.ClientException(response)

        elif response and response.status_code != 200:
            raise GCalService.InvalidData(response)

        try:
            response_model = json.loads(response.body, object_hook=lambda d: namedtuple('Response', d.keys())(*d.values()))
            return [event.summary for event in response_model.items]

        except Exception as e:
            raise GCalService.InvalidData(e)

    class ClientException(Exception):
        pass

    class InvalidData(Exception):
        pass
