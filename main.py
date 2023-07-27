import logging

import config
import podcast_info

# from utils import adobe_podcast, audio_conversion, captivate_api, download_yt, spotify, upload_video

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


def prompt_user_for_playlist():
    playlists = config.playlists
    for i, playlist in enumerate(playlists, start=1):
        print(f"{i}. Playlist Name: {playlist['name']}")

    choice = int(input("Enter the number of the playlist you want to select: "))
    selected_playlist = playlists[choice - 1]
    podcast = podcast_info.PodcastInfo(selected_playlist)
    return podcast


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
