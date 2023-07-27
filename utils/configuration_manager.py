import base64
import os
from datetime import datetime

import requests


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
        self.CAPTIVATE_USER_ID = os.getenv("CAPTIVATE_USER_ID")
        self.CAPTIVATE_API_KEY = os.getenv("CAPTIVATE_API_KEY")

        self.pls = {
            "show_id": os.getenv("PLS_SHOW_ID"),
            "spotify_id": os.getenv("PLS_SPOTIFY_ID"),
            "dir": os.getenv("PLS_DIR"),
            "apple_url": os.getenv("PLS_APPLE_URL"),
            "rss": os.getenv("PLS_RSS"),
            "playlist_id": os.getenv("PLS_PLAYLIST_ID"),
        }
        self.gittin = {
            "show_id": os.getenv("GITTIN_SHOW_ID"),
            "spotify_id": os.getenv("GITTIN_SPOTIFY_ID"),
            "dir": os.getenv("GITTIN_DIR"),
            "apple_url": os.getenv("GITTIN_APPLE_URL"),
            "rss": os.getenv("GITTIN_RSS"),
            "playlist_id": os.getenv("GITTIN_PLAYLIST_ID"),
        }
        self.halacha = {
            "show_id": os.getenv("HALACHA_SHOW_ID"),
            "spotify_id": os.getenv("HALACHA_SPOTIFY_ID"),
            "dir": os.getenv("HALACHA_DIR"),
            "apple_url": os.getenv("HALACHA_APPLE_URL"),
            "rss": os.getenv("HALACHA_RSS"),
            "playlist_id": os.getenv("HALACHA_PLAYLIST_ID"),
        }
        self.kolel = {
            "show_id": os.getenv("KOLEL_SHOW_ID"),
            "spotify_id": os.getenv("KOLEL_SPOTIFY_ID"),
            "dir": os.getenv("KOLEL_DIR"),
            "apple_url": os.getenv("KOLEL_APPLE_URL"),
            "rss": os.getenv("KOLEL_RSS"),
            "playlist_id": os.getenv("KOLEL_PLAYLIST_ID"),
        }
        self.sg_chassidus = {
            "show_id": os.getenv("SG_CHASSIDUS_SHOW_ID"),
            "spotify_id": os.getenv("SG_CHASSIDUS_SPOTIFY_ID"),
            "dir": os.getenv("SG_CHASSIDUS_DIR"),
            "apple_url": os.getenv("SG_CHASSIDUS_APPLE_URL"),
            "rss": os.getenv("SG_CHASSIDUS_RSS"),
            "playlist_id": os.getenv("SG_CHASSIDUS_PLAYLIST_ID"),
        }
        self.shuchat = {
            "show_id": os.getenv("SHUCHAT_SHOW_ID"),
            "spotify_id": os.getenv("SHUCHAT_SPOTIFY_ID"),
            "dir": os.getenv("SHUCHAT_DIR"),
            "apple_url": os.getenv("SHUCHAT_APPLE_URL"),
            "rss": os.getenv("SHUCHAT_RSS"),
            "playlist_id": os.getenv("SHUCHAT_PLAYLIST_ID"),
        }
        self.rm_torah = {
            "show_id": os.getenv("RM_TORAH_SHOW_ID"),
            "spotify_id": os.getenv("RM_TORAH_SPOTIFY_ID"),
            "dir": os.getenv("RM_TORAH_DIR"),
            "apple_url": os.getenv("RM_TORAH_APPLE_URL"),
            "rss": os.getenv("RM_TORAH_RSS"),
            "playlist_id": os.getenv("RM_TORAH_PLAYLIST_ID"),
        }
        self.rm_maamor = {
            "show_id": os.getenv("RM_MAAMOR_SHOW_ID"),
            "spotify_id": os.getenv("RM_MAAMOR_SPOTIFY_ID"),
            "dir": os.getenv("RM_MAAMOR_DIR"),
            "apple_url": os.getenv("RM_MAAMOR_APPLE_URL"),
            "rss": os.getenv("RM_MAAMOR_RSS"),
            "playlist_id": os.getenv("RM_MAAMOR_PLAYLIST_ID"),
        }
        self.rm_tanya = {
            "show_id": os.getenv("RM_TANYA_SHOW_ID"),
            "spotify_id": os.getenv("RM_TANYA_SPOTIFY_ID"),
            "dir": os.getenv("RM_TANYA_DIR"),
            "apple_url": os.getenv("RM_TANYA_APPLE_URL"),
            "rss": os.getenv("RM_TANYA_RSS"),
            "playlist_id": os.getenv("RM_TANYA_PLAYLIST_ID"),
        }
        self.rm_happy = {
            "show_id": os.getenv("RM_HAPPY_SHOW_ID"),
            "spotify_id": os.getenv("RM_HAPPY_SPOTIFY_ID"),
            "dir": os.getenv("RM_HAPPY_DIR"),
            "apple_url": os.getenv("RM_HAPPY_APPLE_URL"),
            "rss": os.getenv("RM_HAPPY_RSS"),
            "playlist_id": os.getenv("RM_HAPPY_PLAYLIST_ID"),
        }

        self.IMGUR_CLIENT_ID = os.getenv("IMGUR_CLIENT_ID")
        self.IMGUR_CLIENT_SECRET = os.getenv("IMGUR_CLIENT_SECRET")

        self.PROJECT_DIR = os.getenv("PROJECT_DIR")
        self.PLAYWRITE_HEADLESS = True if os.getenv("PLAYWRIGHT_HEADLESS") == "True" else False

        self.CLIENT_ID = os.getenv("CLIENT_ID")
        self.CLIENT_SECRET = os.getenv("CLIENT_SECRET")

        self.KOLEL_SPOTIFY_ID = os.getenv("KOLEL_SPOTIFY_ID")

        self.ANCHOR_EMAIL = os.getenv("ANCHOR_EMAIL")
        self.ANCHOR_PASSWORD = os.getenv("ANCHOR_PASSWORD")
        self.LOAD_THUMBNAIL = True if os.getenv("LOAD_THUMBNAIL") == "True" else False
        self.PUPETEER_HEADLESS = False
        self.CAPTIVATE_TOKEN = None
        self.SPOTIFY_TOKEN = None
        self.SPOTIFY_PODCAST_PUBLISH = True if os.getenv("SPOTIFY_PODCAST_PUBLISH") == "True" else False
        self.YOUTUBE_API = os.getenv("YOUTUBE_API")
        self.KOLEL_YOUTUBE_CHANNEL_ID = os.getenv("KOLEL_YOUTUBE_CHANNEL_ID")
        self.TINY_URL_API_KEY = os.getenv("TINY_URL_API_KEY")

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
            self.SPOTIFY_TOKEN = self._get_spotify_access_token(self.CLIENT_ID, self.CLIENT_SECRET)
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
