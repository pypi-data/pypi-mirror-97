"""Abstract base class for API-type streams."""

import abc
import backoff
import copy
import logging
import requests

from datetime import datetime
from typing import Any, Dict, Iterable, List, Optional, Union

from singer.schema import Schema

from singer_sdk.authenticators import APIAuthenticatorBase, SimpleAuthenticator
from singer_sdk.plugin_base import PluginBase as TapBaseClass
from singer_sdk.streams.core import Stream

DEFAULT_PAGE_SIZE = 1000


class RESTStream(Stream, metaclass=abc.ABCMeta):
    """Abstract base class for API-type streams."""

    _page_size: int = DEFAULT_PAGE_SIZE
    _requests_session: Optional[requests.Session]
    rest_method = "GET"

    @property
    @abc.abstractmethod
    def url_base(self) -> str:
        """Return the base url, e.g. 'https://api.mysite.com/v3/'."""
        pass

    def __init__(
        self,
        tap: TapBaseClass,
        name: Optional[str] = None,
        schema: Optional[Union[Dict[str, Any], Schema]] = None,
        path: Optional[str] = None,
    ):
        """Initialize the REST stream."""
        super().__init__(name=name, schema=schema, tap=tap)
        if path:
            self.path = path
        self._http_headers: dict = {}
        self._requests_session = requests.Session()

    @staticmethod
    def _url_encode(val: Union[str, datetime, bool, int, List[str]]) -> str:
        """Encode the val argument as url-compatible string."""
        if isinstance(val, str):
            result = val.replace("/", "%2F")
        else:
            result = str(val)
        return result

    def get_url(self, partition: Optional[dict]) -> str:
        """Return a URL, optionally targeted to a specific partition.
        
        Developers override this method to perform dynamic URL generation.
        """
        url_pattern = "".join([self.url_base, self.path or ""])
        params = copy.deepcopy(dict(self.config))
        if partition:
            params.update(partition)
        url = url_pattern
        for k, v in params.items():
            search_text = "".join(["{", k, "}"])
            if search_text in url:
                url = url.replace(search_text, self._url_encode(v))
        return url

    # HTTP Request functions

    @property
    def requests_session(self) -> requests.Session:
        """Return the session object for HTTP requests."""
        if not self._requests_session:
            self._requests_session = requests.Session()
        return self._requests_session

    @backoff.on_exception(
        backoff.expo,
        (requests.exceptions.RequestException),
        max_tries=5,
        giveup=lambda e: e.response is not None and 400 <= e.response.status_code < 500,
        factor=2,
    )
    def _request_with_backoff(self, prepared_request) -> requests.Response:
        response = self.requests_session.send(prepared_request)
        if response.status_code in [401, 403]:
            self.logger.info("Skipping request to {}".format(prepared_request.url))
            self.logger.info(f"Reason: {response.status_code} - {response.content}")
            raise RuntimeError(
                "Requested resource was unauthorized, forbidden, or not found."
            )
        elif response.status_code >= 400:
            raise RuntimeError(
                f"Error making request to API: {prepared_request.url} "
                f"[{response.status_code} - {response.content}]".replace("\\n", "\n")
            )
        logging.debug("Response received successfully.")
        return response

    def get_url_params(self, partition: Optional[dict]) -> dict:
        """Return a dictionary of values to be used in parameterization."""
        return {}

    def prepare_request(
        self, partition: Optional[dict], next_page_token: Optional[Any]
    ) -> requests.PreparedRequest:
        http_method = self.rest_method
        url: str = self.get_url(partition)
        params: dict = self.get_url_params(partition)
        params = self.insert_next_page_token(
            next_page=next_page_token, params=params
        )
        request_data = self.prepare_request_payload(partition)
        self.logger.info({
            "url": url,
            "params": params,
            "request_data": request_data,
        })
        request = requests.Request(
            method=http_method,
            url=url,
            params=params,
            headers=self.authenticator.http_headers,
            json=request_data,
        ).prepare()
        return request

    def request_records(self, partition: Optional[dict]) -> Iterable[dict]:
        """Request records from REST endpoint(s), returning an iterable Dict of response records.

        If pagination can be detected, pages will be recursed automatically.
        """
        next_page_token = 1
        while next_page_token:
            prepared_request = self.prepare_request(partition, next_page_token=next_page_token)
            resp = self._request_with_backoff(prepared_request)
            for row in self.parse_response(resp):
                yield row
            next_page_token = self.get_next_page_token(resp)

    # Overridable:

    def prepare_request_payload(self, partition: Optional[dict]) -> Optional[dict]:
        """Prepare the data payload for the REST API request.

        By default, no payload will be sent (return None).
        """
        return None

    def get_next_page_token(self, response: requests.Response) -> Any:
        """Return token for identifying next page or None if not applicable."""
        next_page_token = response.headers.get("X-Next-Page", None)
        if next_page_token:
            self.logger.info(f"Next page token retrieved: {next_page_token}")
        return next_page_token

    def insert_next_page_token(self, next_page, params) -> Any:
        """Inject next page token into http request params."""
        if not next_page:
            return params
        if next_page == 1:
            return params
        params["page"] = next_page
        return params

    @property
    def http_headers(self) -> dict:
        """Return headers dict to be used for HTTP requests."""
        result = self._http_headers
        if "user_agent" in self.config:
            result["User-Agent"] = self.config.get("user_agent")
        return result

    # Records iterator

    def get_records(self, partition: Optional[dict]) -> Iterable[Dict[str, Any]]:
        """Return a generator of row-type dictionary objects.

        Each row emitted should be a dictionary of property names to their values.
        """
        state = self.get_stream_or_partition_state(partition)
        for row in self.request_records(partition):
            row = self.post_process(row, state)
            yield row

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result rows."""
        resp_json = response.json()
        if isinstance(resp_json, dict):
            yield resp_json
        else:
            for row in resp_json:
                yield row

    # Abstract methods:

    @property
    def authenticator(self) -> APIAuthenticatorBase:
        """Return an authorization header for REST API requests."""
        return SimpleAuthenticator(stream=self)
