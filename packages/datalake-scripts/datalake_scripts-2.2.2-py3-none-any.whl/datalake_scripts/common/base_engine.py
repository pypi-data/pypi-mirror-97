"""
The base engine is use to request the API to the correct endpoint, and generate the data to be saved by the script.
Extend this engine to give it more functionality.
"""
import os
import json
from json.decoder import JSONDecodeError
from typing import Union
from urllib.parse import urljoin

import requests
from requests import Response

from datalake_scripts.common.logger import logger
from datalake_scripts.common.throttler import throttle
from datalake_scripts.common.token_manager import TokenGenerator


class BaseEngine:
    OCD_DTL_QUOTA_TIME = int(os.getenv('OCD_DTL_QUOTA_TIME', 1))
    OCD_DTL_REQUESTS_PER_QUOTA_TIME = int(os.getenv('OCD_DTL_REQUESTS_PER_QUOTA_TIME', 5))
    logger.debug(f'Throttle selected: {OCD_DTL_REQUESTS_PER_QUOTA_TIME} queries per {OCD_DTL_QUOTA_TIME}s')

    Json = Union[dict, list]  # json like object that can be a dict or root level array

    SET_MAX_RETRY = 3

    def __init__(self, endpoint_config: dict, environment: str, tokens: list):
        self.endpoint_config = endpoint_config
        self.environment = environment
        self.url = self._build_url(endpoint_config, environment)
        self.tokens = tokens
        self.terminal_size = self._get_size_terminal()
        self.token_generator = TokenGenerator(endpoint_config, environment=environment)
        self.headers = None

        self.SET_MAX_RETRY = 3

    def _get_size_terminal(self) -> int:
        """
        Return the terminal size for pretty print
        """
        stty_sizes = os.popen('stty size', 'r').read().split()
        if len(stty_sizes) >= 2:
            return int(stty_sizes[1])
        else:  # Return default terminal size
            return 80

    @throttle(
        period=OCD_DTL_QUOTA_TIME,
        call_per_period=OCD_DTL_REQUESTS_PER_QUOTA_TIME,
    )
    def datalake_requests(self, url: str, method: str, headers: dict, post_body: dict = None):
        """
        Use it to request the API
        """
        self.headers = headers
        tries_left = self.SET_MAX_RETRY

        logger.debug(self._pretty_debug_request(url, method, post_body, headers, self.tokens))

        if not headers.get('Authorization'):
            fresh_tokens = self.token_generator.get_token()
            self.replace_tokens(fresh_tokens)
        while True:
            response = self._send_request(url, method, headers, post_body)
            logger.debug(f'API response:\n{str(response.text)}')
            if response.status_code == 401:
                logger.warning('Token expired or Missing authorization header. Updating token')
                self._token_update(self._load_response(response))
            elif response.status_code == 422:
                logger.warning('Bad authorization header. Updating token')
                logger.debug(f'422 HTTP code: {response.text}')
                self._token_update(self._load_response(response))
            elif response.status_code < 200 or response.status_code > 299:
                logger.error(f'API returned non 2xx response code : {response.status_code}\n{response.text}'
                             f'\n Retrying')
            else:
                try:
                    dict_response = self._load_response(response)
                    return dict_response
                except JSONDecodeError:
                    logger.error('Request unexpectedly returned non dict value. Retrying')
            tries_left -= 1
            if tries_left <= 0:
                logger.error('Request failed: Will return nothing for this request')
                return {}
            # time.sleep(5)

    def _send_request(self, url: str, method: str, headers: dict, data: dict):
        """
        Send the correct http request to url from method [get, post, delete, patch, put].
        Raise a TypeError 'Unknown method to requests {method}' when the method is not one of the above.

        :param url: str
        :param method: str
        :param data: dict
        :param headers: dict
        :param tokens: list
        :return: str
        """
        if method == 'get':
            api_response = requests.get(url=url, headers=headers)
        elif method == 'post':
            api_response = requests.post(url=url, headers=headers, data=json.dumps(data))
        elif method == 'delete':
            api_response = requests.delete(url=url, headers=headers, data=json.dumps(data))
        elif method == 'patch':
            api_response = requests.patch(url=url, headers=headers, data=json.dumps(data))
        elif method == 'put':
            api_response = requests.put(url=url, headers=headers, data=json.dumps(data))
        else:
            logger.debug('ERROR : Wrong requests, please only do [get, post, put, patch, delete] method')
            raise TypeError('Unknown method to requests %s', method)
        return api_response

    def _load_response(self, api_response: Response):
        """
        Load the API response from JSON format to dict.
        The endpoint for events is a bit special, the json.loads() doesn't work for the return format of the API.
        We get for this special case a return dict containing the length of the response i.e.:

            if length of response ==  3 then: no events

        :param: api_response: dict
        :return: dict_response
        """
        if api_response.text.startswith('[') and api_response.text.endswith(']\n'):
            # This condition is for the date-histogram endpoints
            dict_response = {'response_length': len(api_response.text)}
        else:
            dict_response = json.loads(api_response.text)
        return dict_response

    def _token_update(self, dict_response: dict):
        """
        Allow to update token when API response is either Missing Authorization Header
        or Token has expired. Return False is the token has been regenerated.

        :param dict_response: dict
        :return: Bool
        """
        if dict_response.get('msg') == 'Missing Authorization Header':
            fresh_tokens = self.token_generator.get_token()
            self.replace_tokens(fresh_tokens)
            return False
        elif dict_response.get('msg') == 'Bad Authorization header. Expected value \'Token <JWT>\'':
            fresh_tokens = self.token_generator.get_token()
            self.replace_tokens(fresh_tokens)
            return False
        elif dict_response.get('msg') == 'Token has expired':
            fresh_tokens = self.token_generator.refresh_token(self.tokens[1])
            self.replace_tokens(fresh_tokens)
            return False

        return True

    def replace_tokens(self, fresh_tokens: dict):
        access_token = fresh_tokens["access_token"]
        # Update of the refresh token is optional
        refresh_token = fresh_tokens.get('refresh_token', self.tokens[1].replace('Token ', ''))

        self.tokens = [f'Token {access_token}', f'Token {refresh_token}']
        self.headers['Authorization'] = self.tokens[0]

    def _pretty_debug_request(self, url: str, method: str, data: dict, headers: dict, tokens: list):
        """
        Return pretty debug string

        :param url: str
        :param method: str
        :param data: dict
        :param headers: dict
        :param tokens: list
        :return: str
        """
        debug = ('-' * self.terminal_size +
                 'DEBUG - datalake_requests:\n' +
                 f' - url: \n{url}\n' +
                 f' - method: \n{method}\n' +
                 f' - headers: \n{headers}\n' +
                 f' - data: \n{data}\n' +
                 f' - token: \n{tokens[0]}\n' +
                 f' - refresh_token: \n{tokens[1]}\n' +
                 '-' * self.terminal_size)
        return debug

    def _build_url(self, endpoint_config: dict, environment: str):
        """To be implemented by each subclass"""
        raise NotImplemented()

    def _build_url_for_endpoint(self, endpoint_name):
        base_url = urljoin(self.endpoint_config['main'][self.environment], self.endpoint_config['api_version'])
        enpoints = self.endpoint_config['endpoints']
        return urljoin(base_url, enpoints[endpoint_name], allow_fragments=True)
