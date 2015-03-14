__author__ = 'bromix'

from resources.lib.kodion import simple_requests as requests


class Client():
    def __init__(self):
        pass

    def get_categories(self):
        return self._perform_request(url='http://www.clipfish.de/devmobileapp/metachannels')

    def _perform_request(self, url, method='GET', headers=None, post_data=None, params=None, allow_redirects=True):
        # params
        if not params:
            params = {}
            pass
        _params = {}
        _params.update(params)

        # headers
        if not headers:
            headers = {}
            pass
        _headers = {
            'User-Agent': 'Dalvik/1.6.0 (Linux; U; Android 4.4.2; GT-I9505 Build/KOT49H)',
            'Accept-Encoding': 'gzip'}
        _headers.update(headers)

        # url
        _url = url

        result = None

        if method == 'GET':
            result = requests.get(_url, params=_params, headers=_headers, verify=False, allow_redirects=allow_redirects)
            pass
        elif method == 'POST':
            result = requests.post(_url, data=post_data, params=_params, headers=_headers, verify=False,
                                   allow_redirects=allow_redirects)
            pass
        elif method == 'PUT':
            result = requests.put(_url, data=post_data, params=_params, headers=_headers, verify=False,
                                  allow_redirects=allow_redirects)
            pass
        elif method == 'DELETE':
            result = requests.delete(_url, params=_params, headers=_headers, verify=False,
                                     allow_redirects=allow_redirects)
            pass

        if result is None:
            return {}

        return result.json()
