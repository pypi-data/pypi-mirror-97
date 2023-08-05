import json
from requests import Session


class Connection:
    _allowed_methods = ['get', 'post', 'delete']

    def __init__(self, api_user, passwd,  *, proxy_server=None, proxy_port=8080):
        self.__user = api_user
        self.__pass = passwd
        self.session = None
        self.proxy = {}
        self.set_proxy(proxy_server, proxy_port)

    def set_proxy(self, proxy_server, proxy_port):
        if proxy_server and proxy_port:
            self.proxy = {
                'http': 'http://{proxy_server}:{proxy_port}',
                'https': 'https://{proxy_server}:{proxy_port}'
            }

    def get_session(self):
        session = Session()
        session.auth = (self.__user, self.__pass)
        session.proxy = self.proxy

        return session

    def request(self, url, method, *, data={}, headers={}):
        if method not in self._allowed_methods:
            raise ValueError(f'method must be one of {self._allowed_methods}')

        if method == 'post':
            headers['x-csrf-token'] = ''
            headers['Content-Type'] = 'application/json'

        if self.session is None:
            self.session = self.get_session()

        response = self.session.request(
            method,
            url,
            data=json.dumps(data),
            headers=headers)
        response.raise_for_status()

        try:
            response = response.json()
        except json.decoder.JSONDecodeError:
            response = response.text

        return response
