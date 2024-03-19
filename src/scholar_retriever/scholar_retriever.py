import logging
import random
from logging import NullHandler
from typing import Callable, Tuple

import requests

from .utils.tools import HttpHeadersTemplate

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(NullHandler())


class ScholarWebRetriever(object):
    """
    A Base class for retrieving web content from Google scholar web site.
    """

    HL_DEFAULT = "en"

    def __init__(self, get_request_args: Callable[[], dict]) -> None:
        """
        Initialize the ScholarWebRetriever object.

        :param get_request_args: A callable that returns arguments for the GET request.
        :type get_request_args: Callable[[], dict]
        """

        self.get_request_args = get_request_args
        if self.get_request_args is None:
            self.get_request_args = self._default_get_request_args

        self._hl = self.HL_DEFAULT

        # params used for request call
        self._params = {}

    @property
    def language(self):
        """
        The language used for requests to google scholar.
        .. note:

            See https://sites.google.com/site/tomihasa/google-language-codes for a 
            full list of Google Web Interface Language Codes

        """
        return self.params.get("hl", ScholarWebRetriever.HL_DEFAULT)

    @language.setter
    def language(self, new_lang: str):
        """
        Set the language for requests to google scholar.

        :param new_lang: The new language to set.
        :type new_lang: str
        """
        self._hl = new_lang
        self.add_params(hl=self._hl)

    ### params property functions

    @property
    def params(self):
        """
        Params used on the GET request.
        """
        return self._params

    @params.setter
    def params(self, new_params: dict):
        self._params = new_params

    def add_params(self, **kwargs):
        """
        Add or update params to use in the GET request.
        """
        self._params.update(kwargs)

        # Remove items with None value
        self._params = {
            key: value for key, value in self._params.items() if value is not None
        }

    ### request_params_callback property functions

    @property
    def request_args_callback(self) -> Callable[[], dict]:
        """
        Callback function that returns additional arguments (as a dict) to use in the request call.

        This function must return a dict with kwargs to be use on requests.get() call
        
        .. note:

            This is useful for proxy and/or user-agent rotation.

        """
        return self.get_request_args

    @request_args_callback.setter
    def request_args_callback(self, get_request_args_cb: Callable[[], dict]) -> None:
        """Set a callback function for pass extra args on request call.

        This is useful for proxy and/or user-agent rotation.

        :param get_request_params: callback function that return a dict with kwargs to be use on requests.get() call
        :type get_request_params: Callable[ [], dict ]
        """
        self.get_request_args = get_request_args_cb
        if self.get_request_args is None:
            self.get_request_args = self._default_get_request_args


    def reload_web_content(self, retry: int = 3) -> Tuple[bool, str]:
        """
        Reloads the web content from the specified URL endpoint.
        :param retry: The number of retries if the request fails initially. Default is 3.
        :type retry: int, optional
        :return: A tuple indicating success (``True``) or failure (``False``) along with an error message.
        :rtype: tuple[bool, str]
        """
        error = ""
        while retry > 0:
            try:
                kwargs = self.get_request_args()
                resp = requests.request(
                    "GET", self.URL_ENDPOINT, params=self._params, **kwargs
                )
                logger.info(
                    f"Sending request in {self.URL_ENDPOINT} with {self._params}"
                )
                resp.raise_for_status()
                # print(resp.content)
                self.html = resp.content
                break
                # print(json.dumps( ans, indent=2, ensure_ascii=False ))
                # print( ans['profiles'][1]['name'] )
            except Exception as e:
                print(e)
                print("Details:")
                print(f"Headers-req: {kwargs}")
                print(f"Headers-resp: {resp.headers}")
                error = e.__str__
                self.html = None
                retry -= 1

        if retry == 0:
            return (False, error)

        return (True, "Success")

    def get_html(self):
        """
        Get the raw HTML content retrieved from the request call..
        """
        return self.html

    @staticmethod
    def _default_get_request_args() -> dict:
        """
        Generate default request arguments.

        This function returns a dict with default headers.
        """
        headers = random.choice(HttpHeadersTemplate.DEFAULT_TEMPLATES)

        return {
            "headers": headers,
        }


class PaginateBase:
    """Actuate like an interface for paginated webs."""

    def __init__(self) -> None:
        pass

    def next_page(self) -> bool:
        raise Exception(
            "This function must be implemented by classes that inherit from Paginate"
        )

    def prev_page(self) -> bool:
        raise Exception(
            "This function must be implemented by classes that inherit from Paginate"
        )
