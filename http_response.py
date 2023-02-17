class HTTPResponse:
    def __init__(self, status_code: int, body: str) -> None:
        self.status_code = status_code
        self.body = body
