import logging

import podcast.config as config

from .utils import (  # NOQA: F401
    adobe_podcast,
    audio_conversion,
    captivate_api,
    download_yt,
    spotify,
    tiny_url,
    upload_video,
)
from .utils.configuration_manager import ConfigurationManager, LocalMedia, PodcastInfo  # NOQA: F401

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


def create_show_short_links(postcast: PodcastInfo):
    """
    Create tinyurl on the my.shiurimm.net domain for the
    podcast on various platforms like apple, google, spotify, YouTube.
    """
    creator: tiny_url.TinyURLAPI = tiny_url.TinyURLAPI(config.TINYURL_API_KEY)
    print(f"Apple: {postcast.apple_url}")
    apple_url = creator.get_or_create_alias_url(postcast.apple_url, postcast.name + "-Apple")
    print(f"Apple: {apple_url}")

    # google_url = creator.get_or_create_alias_url(postcast.google_url, postcast.name + "-Google")
    # print(f"Google: {google_url}")

    spotify_long_url = "https://open.spotify.com/show/" + postcast.spotify_id
    spotify_url = creator.get_or_create_alias_url(spotify_long_url, postcast.name + "-Spotify")
    print(f"Spotify: {spotify_url}")

    youtube_long_url = "https://www.youtube.com/playlist?list=" + postcast.playlist_id
    youtube_url = creator.get_or_create_alias_url(youtube_long_url, postcast.name + "-YouTube")
    print(f"YouTube: {youtube_url}")


def prompt_user_for_playlist():
    playlists = config.playlists
    for i, playlist in enumerate(playlists, start=1):
        print(f"{i}. Playlist Name: {playlist['name']}")

    choice = int(input("Enter the number of the playlist you want to select: "))
    selected_playlist = playlists[choice - 1]
    podcast = PodcastInfo(selected_playlist)
    return podcast


def file_to_captivate(
    podcast: PodcastInfo,
    file: str,
    title: str = None,
    desc: str = "",
    artwork: str = "",
    publish: bool = True,
    enhance: bool = False,
    episode_num: str = "1",
) -> LocalMedia:
    if title is None:
        title = file.split("/")[-1].split(".")[0]

    media: LocalMedia = LocalMedia(file_name=file, title=title, description=title + "\n" + desc, thumbnail=artwork)
    if enhance:
        media.file_name = adobe_podcast.enhance_podcast(media.file_name, config_manager)
    captivate_api.publish_podcast(media, podcast, config_manager, episode_num, publish=True)
    return media


def file_to_youtube(podcast: PodcastInfo, file: str, title: str = None, desc: str = "", artwork: str = ""):
    if title is None:
        title = file.split("/")[-1].split(".")[0]

    media: LocalMedia = LocalMedia(file_name=file, title=title, description=title + "\n" + desc, thumbnail=artwork)

    media.file_name = audio_conversion.create_video_from_audio_and_picture(
        file, artwork, podcast.dir + "/" + title + ".mp4"
    )
    print("Uploading video to YouTube")
    youtube_url = upload_video.upload_video_with_options(
        media, privacyStatus="private", playlist_id=podcast.playlist_id, channel_id=podcast.channel_id
    )
    print(f"Video uploaded to YouTube: {youtube_url}")


def youtube_to_captivate(
    podcast: PodcastInfo, url: str, artwork: str = "", publish: bool = True, enhance: bool = False
):
    media: LocalMedia = download_yt.download_youtube_video(url)
    if artwork != "":
        media.thumbnail = artwork
    if enhance:
        media.file_name = adobe_podcast.enhance_audio(media.file_name)


def main():
    podcast = prompt_user_for_playlist()
    print(f"Selected playlist: {podcast.name}")

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
