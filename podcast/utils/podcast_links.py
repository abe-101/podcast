import feedparser
import requests
from bs4 import BeautifulSoup

from .configuration_manager import ConfigurationManager
from .spotify import get_latest_spotify_episode_link


class Links:
    def __init__(self, apple, spotify):
        self.youtube = None
        self.apple = apple
        self.spotify = spotify


def get_episode_links(episode_title, show, config: ConfigurationManager):
    captivate_link = get_captivate_link(show["rss"], episode_title)
    print(captivate_link)
    if show["apple_url"] != "":
        apple_link = get_apple_link(show["apple_url"], episode_title)
    else:
        apple_link = None
    spotify_link = get_latest_spotify_episode_link(episode_title, show["spotify_id"], config)

    return {"apple": apple_link, "spotify": spotify_link}


def get_youtube_id(youtube_channel, episode_title):
    pass


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
