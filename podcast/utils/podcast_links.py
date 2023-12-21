import re

import feedparser
import requests
from bs4 import BeautifulSoup

from podcast.utils.apple import get_shows_apple_episode_links
from podcast.utils.configuration_manager import ConfigurationManager, PodcastInfo
from podcast.utils.spotify import get_spotify_episode_links
from podcast.utils.tiny_url import TinyURLAPI
from podcast.utils.whatsapp import send_whatsapp_message

# from discord import SyncWebhook


class Links:
    def __init__(self, title, short_name, podcast: PodcastInfo, config: ConfigurationManager):
        self.podcast: PodcastInfo = podcast
        self.config: ConfigurationManager = config
        self.title = title
        self.short_name = short_name
        self.author = podcast.author
        self.apple = get_shows_apple_episode_links(podcast.apple_id).get(title)
        if not self.apple:
            self.apple = get_apple_link(podcast.apple_url, title)
        self.spotify = get_spotify_episode_links(podcast.spotify_id, config).get(title)
        self.captivatefm = get_captivatefm_episode_links(podcast.rss).get(title)
        self.youtube = get_youtube_id_from_podcast(podcast, title)

        self.youtute_short = None
        self.apple_short = ""
        self.spotify_short = None
        self.captivatefm_short = None

    def get_tiny_urls(self, tags):
        short_name = self.short_name
        create = TinyURLAPI(self.config.TINY_URL_API_KEY)
        youtube_tag = tags.copy()
        youtube_tag.append("youtube")
        self.youtube_short = create.get_or_create_alias_url(
            f"https://youtu.be/{self.youtube}",  # noqa E231
            f"{short_name}-YouTube",
            tags=youtube_tag,
        )
        spotify_tag = tags.copy()
        spotify_tag.append("spotify")
        self.spotify_short = create.get_or_create_alias_url(
            self.spotify,
            f"{short_name}-Spotify",
            tags=spotify_tag,
        )
        apple_tag = tags.copy()
        apple_tag.append("apple")
        self.apple_short = create.get_or_create_alias_url(
            self.apple,
            f"{short_name}-Apple",
            tags=apple_tag,
        )
        captivatefm_tag = tags.copy()
        captivatefm_tag.append("captivatefm")
        self.captivatefm_short = create.get_or_create_alias_url(
            self.captivatefm,
            f"{short_name}",
            tags=captivatefm_tag,
        )

    def __str__(self):
        return f"""

YouTube - {self.youtube}
Spotify - {self.spotify}
Apple - {self.apple}
Captivate.fm - {self.captivatefm}
"""

    def whatsapp_str(self):
        return f"""
*{self.title}*

*YouTube Link*

{self.youtube_short}

*Spotify Link*

{self.spotify_short}

*Apple Link*

{self.apple_short}

{self.captivatefm_short}
"""  # noqa E222, E221

    def default_template(self) -> str:
        """Returns the default template for WhatsApp."""
        return """
*{title}*

*YouTube Link*
{youtube}

*Spotify Link*
{spotify}

*Apple Link*
{apple}

{captivatefm}
"""

    def generate_template(self, template: str = None) -> str:
        """Generates a string based on the provided template or the default template if none is given."""

        if template is None:
            template = self.default_template()

        # Replace placeholders with actual values
        output = template.replace("{title}", self.title)
        output = output.replace("{youtube}", self.youtube_short)
        output = output.replace("{spotify}", self.spotify_short)
        output = output.replace("{apple}", self.apple_short)
        if "{captivatefm}" in template and self.captivatefm:
            output = output.replace("{captivatefm}", self.captivatefm_short)

        # webhook = SyncWebhook.from_url(self.config.DISCORD_WEBHOOK_URL)
        output = output.strip()
        # webhook.send(output)

        return output

    def send_whatsapp_msg(self):
        send_whatsapp_message(self.title, self.author, self.short_name, self.config)


def get_youtube_id_from_podcast(podcast: PodcastInfo, episode_title):
    rss_url = "https://feeds.captivate.fm/" + podcast.rss
    feed = feedparser.parse(rss_url)
    for episode in feed.entries:
        if episode["title"] == episode_title:
            return get_youtube_id_from_text(episode["summary"])


def get_youtube_id_from_text(text: str):
    pattern = r"(?:youtube\.com\/watch\?v=|youtu.be\/)([A-Za-z0-9_-]+)"
    match = re.search(pattern, text)
    if match:
        video_id = match.group(1)
        return video_id
    else:
        return None


def choose_episode(podcast: PodcastInfo):
    rss_url = "https://feeds.captivate.fm/" + podcast.rss
    feed = feedparser.parse(rss_url)
    episodes = []
    for episode in feed.entries[:5]:
        episodes.append(episode["title"])
    for i, episode in enumerate(episodes):
        print(f"{i + 1}. {episode}")
    choice = int(input("Choose an episode: "))
    return episodes[choice - 1]


def get_episode_links(episode_title, podcast: PodcastInfo, config: ConfigurationManager):
    capt = get_captivatefm_episode_links(podcast.rss)
    spotify = get_spotify_episode_links(podcast.spotify_id, config)
    apple = get_shows_apple_episode_links(podcast.apple_id)
    return Links(episode_title, apple.get(episode_title), spotify.get(episode_title), capt.get(episode_title))


def check_for_existing_episode_by_title(title: str, rss: str) -> bool:
    """
    Checks if an episode with the given title already exists in the podcast's RSS feed.

    Parameters:
    - title (str): The title of the episode.
    - rss (str): The RSS URL of the podcast.

    Returns:
    - bool: episode_id if the episode exists, False otherwise.
    """
    rss_url = "https://feeds.captivate.fm/" + rss
    feed = feedparser.parse(rss_url)

    for episode in feed.entries:
        if episode["title"] == title:
            return episode["id"]

    return False


def get_recent_episode_number(podcast: PodcastInfo):
    rss_url = "https://feeds.captivate.fm/" + podcast.rss
    feed = feedparser.parse(rss_url)
    if not feed.entries:  # Check if the entries list is empty
        return 1
    return int(feed.entries[0]["podcast_episode"])


def get_captivatefm_episode_links(rss: str) -> dict[str, str]:
    """
    Fetches the podcast episode names and their URLs from Captivate.fm based on the given RSS URL.

    Parameters:
    - rss_url (str): The RSS URL of the podcast.

    Returns:
    - Dict[str, str]: A dictionary where the key is the episode's name and the value is its link.
    """
    rss_url = "https://feeds.captivate.fm/" + rss
    feed = feedparser.parse(rss_url)

    episodes = {}

    for episode in feed.entries:
        title = episode["title"]
        link = episode["links"][0]["href"]
        episodes[title] = link

    return episodes


def get_captivate_link(rss, episode_title):
    rss_url = "https://feeds.captivate.fm/" + rss
    feed = feedparser.parse(rss_url)
    for episode in feed.entries:
        if episode["title"] == episode_title:
            return episode["link"]
    return None


def get_apple_link(podcast_url, episode_title):
    """
    Fetches the Apple Podcasts URL for a specific podcast episode based on the episode title.

    Args:
        podcast_url (str): The URL of the Apple Podcasts page for the podcast.
        episode_title (str): The title of the desired podcast episode.

    Returns:
        str: The episode URL that matches the given title, or None if no match found.
    """
    if podcast_url == "":
        return None
    # Send an HTTP GET request to the podcast URL
    response = requests.get(podcast_url)

    # Parse the HTML response using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Extract the episode link from the HTML structure
    for link in soup.find_all("a"):
        href = link.get("href")
        title = link.text.strip()  # Get the text content of the anchor tag and strip leading/trailing spaces
        if href.startswith("https://podcasts.apple.com/us/podcast/") and title == episode_title:
            return href

    # Return None if no match found
    return ""
