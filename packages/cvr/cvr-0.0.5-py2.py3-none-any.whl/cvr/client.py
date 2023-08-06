from cvr.errors import UnauthorizedError, NotFoundError
from requests_toolbelt.sessions import BaseUrlSession
from http import HTTPStatus


_BASE_URL = 'https://api.cvr.dev/api/'


class Client:
    def __init__(self, api_key):
        self._session = BaseUrlSession(_BASE_URL)
        self._session.headers.update({'Authorization': api_key})

    def test_api_key(self):
        resp = self._session.get('test/apikey')
        self._handle_status_code(resp)

    def _handle_status_code(self, response):
        if response.status_code == HTTPStatus.UNAUTHORIZED:
            raise UnauthorizedError('Invalid API key')
        if response.status_code == HTTPStatus.NOT_FOUND:
            raise NotFoundError('Entity not found')
