class HTTPClientSpy:
    def __init__(self) -> None:
        self.requested_urls = []

    def get(self, url) -> None:
        self.requested_urls.append(url)
