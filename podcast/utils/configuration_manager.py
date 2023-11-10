import base64
from datetime import datetime

import requests

from podcast import config


class PodcastInfo:
    def __init__(self, data: dict):
        self.name: str = data.get("name", "")
        self.author: str = data.get("author", "")
        self.podcast_show_id: str = data.get("podcast_show_id", "")
        self.spotify_id: str = data.get("spotify_id", "")
        self.dir: str = data.get("dir", "")
        self.apple_url: str = data.get("apple_url", "")
        self.rss: str = data.get("rss", "")
        self.playlist_id: str = data.get("playlist_id", "")
        self.google_url: str | None = data.get("google_url", None)
        self.channel_id: str | None = data.get("channel_id", None)
        self.apple_id: str | None = self.apple_url[-10:] if self.apple_url else None


class LocalMedia:
    def __init__(
        self,
        file_name: str,
        title: str,
        description: str,
        thumbnail: str = None,
        url: str = "",
        upload_date: datetime = datetime.now(),
    ):
        self.file_name = file_name
        self.title = title
        self.description = description
        self.url = url
        self.thumbnail = thumbnail
        self.upload_date = upload_date
        self.captivate_id = None
        self.path_to_video = None
        self.keywords = ""

    def __str__(self):
        return (
            f"Media: {self.title} ({self.file_name})\n"
            f"Description: {self.description}\n"
            f"URL: {self.url}\n"
            f"Thumbnail: {self.thumbnail}\n"
            f"Upload date: {self.upload_date}"
        )

    def set_upload_date_from_timestamp(self, timestamp: int):
        try:
            if timestamp is None:
                self.upload_date = datetime.now()
            else:
                self.upload_date = datetime.fromtimestamp(timestamp)
        except ValueError:
            print("Error: Invalid timestamp." + str(timestamp))

    def set_upload_date_from_string(self, date_str: str):
        try:
            self.upload_date = datetime.strptime(date_str, "%Y%m%d")
        except ValueError:
            print("Error: Invalid date format. Use YYYYMMDD." + date_str)


class ConfigurationManager:
    def __init__(self):
        self.CAPTIVATE_USER_ID = config.CAPTIVATE_USER_ID
        self.CAPTIVATE_API_KEY = config.CAPTIVATE_API_KEY

        self.IMGUR_CLIENT_ID = config.IMGUR_CLIENT_ID
        self.IMGUR_CLIENT_SECRET = config.IMGUR_CLIENT_SECRET

        # self.PROJECT_DIR = os.getenv("PROJECT_DIR")
        self.PLAYWRITE_HEADLESS = True if config.PLAYWRIGHT_HEADLESS == "True" else False

        self.SPOTIFY_CLIENT_ID = config.SPOTIFY_CLIENT_ID
        self.SPOTIFY_CLIENT_SECRET = config.SPOTIFY_CLIENT_SECRET

        self.CAPTIVATE_TOKEN = None
        self.SPOTIFY_TOKEN = None
        self.YOUTUBE_API = config.YOUTUBE_API_KEY
        self.TINY_URL_API_KEY = config.TINYURL_API_KEY
        self.DISCORD_WEBHOOK_URL = config.DISCORD_WEBHOOK_URL
        self.WHATSAPP_TOKEN = config.WHATSAPP_TOKEN
        self.WHATSAPP_BUISNESS_ID = config.WHATSAPP_BUISNESS_ID
        self.WHATSAPP_SENDER_ID = config.WHATSAPP_SENDER_ID
        self.WHATSAPP_RECIPIENT_NUMBER = config.WHATSAPP_RECIPIENT_NUMBER

    def get_captivate_token(self):
        if self.CAPTIVATE_TOKEN is None:
            # Get the Captivate token
            print("Getting captivate token from api")
            self.CAPTIVATE_TOKEN = self._get_captivate_token()
        return self.CAPTIVATE_TOKEN

    def _get_captivate_token(self) -> str | None:
        """
        This function gets a token from the captivate.fm API, using the user_id and api_key as authentication.

        :param user_id: The user_id of the account to get a token for
        :type user_id: str
        :param api_key: The api_key for the account
        :type api_key: str
        :return: The token from the API
        :rtype: Union[str, None]
        :raise: Exception if the API request fails.
        """
        url = "https://api.captivate.fm/authenticate/token"

        payload = {
            "username": self.CAPTIVATE_USER_ID,
            "token": self.CAPTIVATE_API_KEY,
        }
        files = []
        headers = {}

        try:
            response = requests.request("POST", url, headers=headers, data=payload, files=files)
            response.raise_for_status()
            r = response.json()
            return r["user"]["token"]
        except requests.exceptions.HTTPError as error:
            print(f"An HTTP error occurred: {error}")
            return

    def get_spotify_token(self):
        if not self.SPOTIFY_TOKEN:
            self.SPOTIFY_TOKEN = self._get_spotify_access_token(self.SPOTIFY_CLIENT_ID, self.SPOTIFY_CLIENT_SECRET)
        return self.SPOTIFY_TOKEN

    def _get_spotify_access_token(self, client_id: str, client_secret: str) -> str:
        """
        Retrieve an access token from the Spotify API using the provided client ID
        and client secret.

        :param client_id: The client ID for the Spotify API.
        :type client_id: str

        :param client_secret: The client secret for the Spotify API.
        :type client_secret: str

        :return: The access token for the Spotify API.
        :rtype: str
        """

        # Encode the client ID and client secret
        client_credentials = f"{client_id}:{client_secret}"
        encoded_credentials = base64.b64encode(client_credentials.encode("ascii")).decode("ascii")

        # Send a request to the Spotify API to fetch an access token
        url = "https://accounts.spotify.com/api/token"
        headers = {"Authorization": f"Basic {encoded_credentials}"}
        data = {"grant_type": "client_credentials"}
        response = requests.post(url, headers=headers, data=data)

        # Check if the request was successful
        if response.status_code != 200:
            raise ValueError("Failed to obtain Spotify access token")

        # Return the access token
        access_token = response.json()["access_token"]
        return access_token
