import logging
import os
import time

from tqdm import tqdm

import podcast.config as config
from podcast.utils import (  # NOQA: F401
    adobe_podcast,
    audio_conversion,
    captivate_api,
    download_yt,
    podcast_links,
    spotify,
    tiny_url,
    upload_video,
)
from podcast.utils.configuration_manager import ConfigurationManager, LocalMedia, PodcastInfo  # NOQA: F401

config_manager = ConfigurationManager()

# Configure the logger
logger = logging.getLogger("Podcast")
logger.setLevel(logging.INFO)

# Create a file handler for logging to a file
log_file = "podcast.log"
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.INFO)

# Create a console handler for logging to the console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create a formatter to format the log messages
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)


def hello_world():
    print("Hello World!")


def get_file_extension(file_path: str, file_name: str):
    """
    file_name is without an extension
    check if file name exist with either mp3 or m4a extension
    and return file name with extension
    """
    mp3_file = file_path + "/" + file_name + ".mp3"
    m4a_file = file_path + "/" + file_name + ".m4a"
    if os.path.exists(mp3_file):
        print("File exists: " + mp3_file)
        return mp3_file
    elif os.path.exists(m4a_file):
        print("File exists: " + m4a_file)
        return m4a_file
    else:
        raise Exception("File does not exist")


def wait_with_progressbar(duration_in_seconds):
    for second_passed in tqdm(range(duration_in_seconds), desc="Waiting", unit="s"):
        seconds_left = duration_in_seconds - second_passed
        minutes_left = seconds_left // 60
        seconds_left %= 60

        # Print the remaining time, overwrite the current line with \r, and flush the output
        print(f"\r{minutes_left}:{seconds_left}", end="", flush=True)
        time.sleep(1)
    print()  # Newline after completion


def create_show_short_links(podcast: PodcastInfo, podcast_name: str = None):
    """
    Create tinyurl on the my.shiurimm.net domain for the
    podcast on various platforms like apple, google, spotify, YouTube.
    """
    if podcast_name is None:
        podcast_name = podcast.name
    creator: tiny_url.TinyURLAPI = tiny_url.TinyURLAPI(config.TINYURL_API_KEY)
    print(f"Apple: {podcast.apple_url}")
    apple_url = creator.get_or_create_alias_url(podcast.apple_url, podcast_name + "-Apple")
    print(f"Apple: {apple_url}")

    # google_url = creator.get_or_create_alias_url(podcast.google_url, podcast.name + "-Google")
    # print(f"Google: {google_url}")

    spotify_long_url = "https://open.spotify.com/show/" + podcast.spotify_id
    spotify_url = creator.get_or_create_alias_url(spotify_long_url, podcast_name + "-Spotify")
    print(f"Spotify: {spotify_url}")

    youtube_long_url = "https://www.youtube.com/playlist?list=" + podcast.playlist_id
    youtube_url = creator.get_or_create_alias_url(youtube_long_url, podcast_name + "-YouTube")
    print(f"YouTube: {youtube_url}")


def prompt_user_for_playlist():
    playlists = config.playlists
    for i, playlist in enumerate(playlists, start=1):
        print(f"{i}. Playlist Name: {playlist['name']}")

    choice = int(input("Enter the number of the playlist you want to select: "))
    selected_playlist = playlists[choice - 1]
    podcast = PodcastInfo(selected_playlist)
    return podcast


def add_audio_to_podcast(podcast: PodcastInfo, file_1: str, file_2: str, episode_id: str, format: str = "mp3"):
    if format == "m4a":
        combined_file = audio_conversion.combine_m4a_files(file_1, file_2)
    else:
        combined_file = audio_conversion.combine_mp3_files(file_1, file_2)
    media_id = captivate_api.upload_media(config_manager, podcast.podcast_show_id, combined_file)
    episode = captivate_api.get_episode(config_manager, episode_id)
    episode_url = captivate_api.update_podcast(
        config=config_manager,
        media_id=media_id,
        shows_id=podcast.podcast_show_id,
        episode_id=episode_id,
        shownotes=episode["shownotes"],
        title=episode["title"],
        date=episode["published_date"],
        status=episode["status"],
        episode_number=episode["episode_number"],
        episode_season=episode["episode_season"],
    )
    print(f"Episode URL: {episode_url}")


def main():
    podcast = prompt_user_for_playlist()
    print(f"Selected playlist: {podcast.name}")
    choice = input("1. YouTube to Captivate.fm, 2. Get show short links: ")
    if choice == "1":
        youtube_id = input("Enter the YouTube ID: ")
        media: LocalMedia = download_yt.download_youtube_video(youtube_id, podcast.dir)
        episode = captivate_api.publish_podcast(local_media=media, podcast=podcast, config=config_manager)
        print(f"Episode: {episode}")
    elif choice == "2":
        podcast_name = input("Enter the short name of the podcast: ")
        create_show_short_links(podcast, podcast_name)

    # name = input("Enter the name of the podcast: ")
    # # Get the latest videos from the selected playlist
    # latest_videos = youtube_module.get_latest_videos(selected_playlist["playlist_id"], limit=15)

    # # Convert the latest videos to podcasts and publish
    # for video in latest_videos:
    #     mp3_file = youtube_module.download_and_convert_to_mp3(video)
    #     enhanced_audio = audio_module.enhance_audio(mp3_file, selected_playlist["adobe_ai_api_key"])
    #     podcast_data = create_podcast_data(video, enhanced_audio, selected_playlist)
    #     captivate_module.publish_podcast(podcast_data, selected_playlist["captivate_api_key"])


if __name__ == "__main__":
    main()
