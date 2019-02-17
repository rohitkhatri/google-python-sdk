import requests
from urllib.parse import urlencode
from google.exceptions import GoogleException


class API:
    _client_id = None
    _client_secret = None
    _api_key = None
    _access_token = None
    _api_base_url = 'https://www.googleapis.com/google/v3'
    _auth_url = 'https://accounts.google.com/o/oauth2/auth'
    _profile_url = 'https://www.googleapis.com/oauth2/v3/userinfo'
    _exchange_code_url = 'https://accounts.google.com/o/oauth2/token'
    _scope = [
        'https://www.googleapis.com/auth/userinfo.profile',
        'https://www.googleapis.com/auth/userinfo.email'
    ]
    _part = 'id,snippet'

    def __init__(self, client_id, client_secret, api_key, access_token=None, api_url=None):
        self._client_id = client_id
        self._client_secret = client_secret
        self._api_key = api_key
        self._access_token = access_token

        if api_url:
            self.api_url = api_url

    def get(self, endpoint, **kwargs):
        if self._access_token:
            kwargs['access_token'] = self._access_token
        else:
            kwargs['api_key'] = self._api_key

        if 'part' not in kwargs:
            kwargs['part'] = self._part

        return self.response(self._get('{}{}'.format(self._api_base_url, endpoint), params=kwargs))

    def post(self, endpoint, **kwargs):
        if self._access_token:
            kwargs['access_token'] = self._access_token
        else:
            kwargs['api_key'] = self._api_key

        return self.response(self._post('{}{}'.format(self._api_base_url, endpoint), params=kwargs))

    def get_auth_url(self, redirect_uri, **kwargs):
        kwargs = {**{
            'response_type': 'code',
            'redirect_uri': redirect_uri,
            'client_id': self._client_id,
            'access_type': 'offline',
            'approval_prompt': 'force'
        }, **kwargs}

        if 'scope' not in kwargs:
            kwargs['scope'] = self._scope

        kwargs['scope'] = ' '.join(kwargs['scope'])

        return '{}?{}'.format(self._auth_url, urlencode(kwargs))

    def exchange_code(self, code, redirect_uri):
        params = {
            'code': code, 'client_id': self._client_id, 'client_secret': self._client_secret,
            'redirect_uri': redirect_uri, 'grant_type': 'authorization_code'
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = self.response(self._post(self._exchange_code_url, params=params, headers=headers))

        if response and 'access_token' in response:
            self._access_token = response['access_token']

        return response

    def refresh_token(self, refresh_token):
        params = {
            'client_id': self._client_id, 'client_secret': self._client_secret, 'refresh_token': refresh_token,
            'grant_type': 'refresh_token'
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = self.response(self._post(self._exchange_code_url, params=params, headers=headers))

        if response and 'access_token' in response:
            self._access_token = response['access_token']

        return response

    def get_token_info(self):
        return self.response(self._get('https://oauth2.googleapis.com/tokeninfo', {
            'access_token': self._access_token
        }))

    def get_profile(self):
        return self.response(self._get(self._profile_url, {
            'access_token': self._access_token
        }))

    @staticmethod
    def _get(url, params=None, **kwargs):
        result = requests.get(url, params=params, **kwargs)
        _response = result.json()

        if _response and 'error' in _response:
            raise GoogleException(_response['error']['code'], _response['error']['message'], result)

        if result.status_code != 200:
            raise GoogleException(result.status_code, result.reason, result)

        return result

    @staticmethod
    def _post(url, params=None, **kwargs):
        result = requests.post(url, data=params, **kwargs)
        _response = result.json()

        if _response and 'error' in _response:
            if isinstance(_response['error'], str):
                raise GoogleException(result.status_code, _response['error'], result)
            else:
                raise GoogleException(_response['error']['code'], _response['error']['message'], result)

        if result.status_code != 200:
            raise GoogleException(result.status_code, result.reason, result)

        return result

    @staticmethod
    def response(response):
        return response.json()
