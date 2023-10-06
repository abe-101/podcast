import json
from enum import Enum
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv

from podcast.utils.configuration_manager import ConfigurationManager

load_dotenv()

config = ConfigurationManager()


def capitalize_url(url):
    parsed_url = urlparse(url)
    domain_parts = parsed_url.netloc.split(".")
    capitalized_domain = ".".join(
        [part.capitalize() if i < len(domain_parts) - 1 else part for i, part in enumerate(domain_parts)]
    )
    capitalized_url = f"{parsed_url.scheme}://{capitalized_domain}{parsed_url.path}"
    return capitalized_url


class Operation(Enum):
    CREATE = "create"
    UPDATE = "update"
    CHANGE = "change"
    DELETE = "delete"
    ARCHIVE = "archive"
    UNARCHIVE = "unarchive"


class URLData:
    def __init__(
        self,
        operation: Operation,
        url: str,
        domain: str,
        alias: str,
        tags: list[str] = None,
        expires_at: str = "",
        metadata: list[str] = None,
    ):
        self.operation = operation
        self.url = url
        self.metadata = metadata if metadata else []
        self.domain = domain
        self.alias = alias
        self.tags = tags if tags else []
        self.expires_at = expires_at

    def to_dict(self) -> dict:
        data = {
            "operation": self.operation.value,
            "url": self.url,
            "domain": self.domain,
            "alias": self.alias,
            "tags": self.tags,
            "expires_at": self.expires_at,
        }

        if self.metadata:
            data["metadata"] = self.metadata

        return data


class CreateAliasUrlError(Exception):
    pass


class TinyURLAPI:
    def __init__(self, api_token):
        self.api_token = api_token
        self.url = "https://api.tinyurl.com/"
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.api_token}",
        }

    def create_alias_url(self, long_url, alias, domain="my.shiurim.net", tags="", expires_at=""):
        try:
            if tags == "":
                tags = []
            payload = json.dumps(
                {
                    "url": long_url,
                    "domain": domain,
                    "alias": alias,
                    "tags": tags,
                    "expires_at": expires_at,
                }
            )

            response = requests.request("POST", self.url + "create", headers=self.headers, data=payload)
            response_data = response.json()

            if response.status_code != 200 or "data" not in response_data or "tiny_url" not in response_data["data"]:
                error_message = response_data.get("error", "Unknown error")
                raise CreateAliasUrlError(error_message)

            return capitalize_url(response_data["data"]["tiny_url"])
        except CreateAliasUrlError as e:
            print("An error occurred:", e)
            raise e

    def get_alias_url(self, alias, domain="my.shiurim.net"):
        response = requests.request("GET", self.url + f"alias/{domain}/{alias}", headers=self.headers)
        response_json = response.json()
        if "data" in response_json and response_json["data"]:
            return capitalize_url(response_json["data"]["tiny_url"])
        else:
            return None

    def get_or_create_alias_url(self, long_url, alias, domain="my.shiurim.net", tags="", expires_at=""):
        if tags == "":
            tags = []
        if long_url is None or long_url == "":
            return ""
        existing_url = self.get_alias_url(alias, domain)
        if existing_url:
            return existing_url
        else:
            return self.create_alias_url(long_url, alias, domain, tags, expires_at)

    def bulk_create_short_urls(self, url_data: list[URLData]) -> str:
        """
        Bulk creates short URLs.

        Parameters:
        - url_data (List[URLData]): List containing the long URLs and their details.
        - bearer_token (str): Token for authentication.
        - api_url (str): API endpoint. Defaults to "https://api.tinyurl.com/bulk".

        Returns:
        - Response text from the server.
        """

        payload = json.dumps({"items": [data.to_dict() for data in url_data]})

        response = requests.request("POST", self.url + "bulk", headers=self.headers, data=payload)
        return response.json()


if "__main__" == __name__:
    # Example usage
    creator = TinyURLAPI(config.TINY_URL_API_KEY)
    url_data = [
        URLData(
            operation=Operation.CREATE,
            url="https://podcasts.apple.com/us/podcast/meseches-gittin-rabbi-shloime-greenwald/id1689640425",
            domain="my.shiurim.net",
            alias="Gittin-Apple-test2",
        ),
    ]
    r = creator.bulk_create_short_urls(url_data)
    print(r)

    # url = creator.get_or_create_alias_url(
    #        "https://podcasts.apple.com/us/podcast/meseches-gittin-rabbi-shloime-greenwald/id1689640425",
    #        "Gittin-Apple",
    #        )
    # print(url)

    # url = creator.get_or_create_alias_url(
    #        "https://open.spotify.com/show/0Cgr6r1gTNNzbln8ghofjH",
    #        "Gittin-Spotify",
    #        )
    # print(url)
    # url = creator.get_or_create_alias_url(
    #        "https://podcasts.google.com/feed/aHR0cHM6Ly9mZWVkcy5jYXB0aXZhdGUuZm0vZ2l0dGlu",
    #        "Gittin-Google",
    #        )
    # print(url)
    # url = creator.get_or_create_alias_url(
    #        "https://www.youtube.com/playlist?list=PLFy3gCT2Rdy-umH9TAvs7VnF8peLPXZRo",
    #        "Gittin-YouTube",
    #        )
    # print(url)
    # url = creator.get_or_create_alias_url(
    #        "https://gittin.captivate.fm/listen",
    #        "Gittin",
    #        )
    # print(url)
