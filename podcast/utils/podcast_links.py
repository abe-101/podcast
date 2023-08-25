import re

import feedparser
import requests
from bs4 import BeautifulSoup

from podcast.utils.apple import get_apple_episode_links
from podcast.utils.configuration_manager import ConfigurationManager, PodcastInfo
from podcast.utils.spotify import get_spotify_episode_links
from podcast.utils.tiny_url import TinyURLAPI


class Links:
    def __init__(self, title, podcast: PodcastInfo, config: ConfigurationManager):
        self.podcast: PodcastInfo = podcast
        self.config: ConfigurationManager = config
        self.title = title
        self.apple = get_apple_episode_links(podcast.apple_id).get(title)
        self.spotify = get_spotify_episode_links(podcast.spotify_id, config).get(title)
        self.captivatefm = get_captivatefm_episode_links(podcast.rss).get(title)
        self.youtube = get_youtube_id_from_podcast(podcast, title)

        self.youtute_short = None
        self.apple_short = None
        self.spotify_short = None
        self.captivatefm_short = None

    def get_tiny_urls(self, short_name: str, tags: str = [""]):
        create = TinyURLAPI(self.config.TINY_URL_API_KEY)
        self.youtube_short = create.get_or_create_alias_url(
            f"https://youtu.be/{self.youtube}",
            f"{short_name}-YouTube",
            tags=tags.append("youtube"),
        )
        self.spotify_short = create.get_or_create_alias_url(
            self.spotify,
            f"{short_name}-Spotify",
            tags=tags.append("spotify"),
        )
        self.apple_short = create.get_or_create_alias_url(
            self.apple,
            f"{short_name}-Apple",
            tags=tags.append("apple"),
        )
        self.captivatefm_short = create.get_or_create_alias_url(
            self.captivatefm,
            f"{short_name}",
            tags=tags.append("captivatefm"),
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

*YouTube*

{self.youtube_short}

*Spotify*

{self.spotify_short}

*Apple*

{self.apple_short}

{self.captivatefm_short}
"""


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


def get_episode_links(episode_title, podcast: PodcastInfo, config: ConfigurationManager):
    capt = get_captivatefm_episode_links(podcast.rss)
    spotify = get_spotify_episode_links(podcast.spotify_id, config)
    apple = get_apple_episode_links(podcast.apple_id)
    return Links(episode_title, apple.get(episode_title), spotify.get(episode_title), capt.get(episode_title))

    # captivate_link = get_captivate_link(podcast.rss, episode_title)
    # if show["apple_url"] != "":
    #    apple_link = get_apple_link(show["apple_url"], episode_title)
    # else:
    #    apple_link = None
    # spotify_link = get_latest_spotify_episode_link(episode_title, show["spotify_id"], config)

    # return {"apple": apple_link, "spotify": spotify_link}


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
    return None


def get_anchor_link(rss_url, episode_title):
    feed = feedparser.parse(rss_url)
    for episode in feed.entries:
        if episode["title"] == episode_title:
            return episode["links"][0]["href"]
    return None


def prepare_sharable_post(links: dict, youtube_id: str, video_title: str):
    template = f"""
{video_title}

YouTube - https://www.youtube.com/watch?v={youtube_id}
Spotify - {links["spotify"]}
Apple - {links["apple"]}
"""
    return template
