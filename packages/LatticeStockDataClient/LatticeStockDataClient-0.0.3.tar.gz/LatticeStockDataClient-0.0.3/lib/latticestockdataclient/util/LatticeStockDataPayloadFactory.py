import logging


class LatticeStockDataPayloadFactory:
    def __init__(self, host, key):
        self.x_rapidapi_host=host
        self.x_rapidapi_key=key
        self._url=None

    def url(self, endpoint):
        self._url = "https://%s/%s" % (self.x_rapidapi_host.rstrip("/"), endpoint.lstrip("/"))
        return self._url

    @property
    def headers(self):
        headers = {
            'x-rapidapi-key': self.x_rapidapi_key,
            'x-rapidapi-host': self.x_rapidapi_host
        }
        return headers
