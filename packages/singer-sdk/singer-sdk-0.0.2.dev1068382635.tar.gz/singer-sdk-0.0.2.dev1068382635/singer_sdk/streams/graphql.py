"""Abstract base class for API-type streams."""

import abc
from typing import Iterable, Optional

from singer_sdk.streams.rest import RESTStream


class GraphQLStream(RESTStream, metaclass=abc.ABCMeta):
    """Abstract base class for API-type streams."""

    query: Optional[str] = None
    path = ""
    rest_method = "POST"

    def prepare_request_payload(self, partition: Optional[dict]) -> Optional[dict]:
        """Prepare the data payload for the GraphQL API request."""
        params = self.get_url_params(partition)
        if self.query is None:
            raise ValueError("Graphql `query` property not set.")
        else:
            query = self.query
        request_data = {
            "query": "query { "
            + (" ".join([l.strip() for l in query.splitlines()]))
            + " }",
            "variables": params,
        }
        self.logger.info(f"Attempting query:\n{query}")
        return request_data

    def parse_response(self, response) -> Iterable[dict]:
        """Parse the response and return an iterator of result rows."""
        resp_json = response.json()
        for row in resp_json["data"][self.name]:
            yield row
