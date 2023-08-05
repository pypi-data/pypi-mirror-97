from .connection import Connection
from .activity import Activity


class Lama:
    def __init__(self, base_url: str, api_user: str, passwd: str, proxy_server=None, proxy_port=None):
        self._base_url = base_url
        self._connection = Connection(
            api_user, passwd, proxy_server=proxy_server, proxy_port=proxy_port)

    def _build_url(self, endpoint_url, params={}):
        return f'{self._base_url}{endpoint_url.format(**params)}'

    def activity(self):
        return Activity(self)
