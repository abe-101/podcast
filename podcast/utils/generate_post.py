#!/usr/bin/python

import os
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

import googleapiclient.errors
from configuration_manager import ConfigurationManager
from dotenv import load_dotenv
from googleapiclient.discovery import build
from podcast_links import Links, get_episode_links, prepare_sharable_post
from rich.console import Console

# from rich import print
from rich.prompt import Prompt
from rich.table import Table
from tiny_url import TinyURLAPI

load_dotenv()

config = ConfigurationManager()

YOUTUBE_TO_ANCHORFM = os.getenv("YOUTUBE_TO_ANCHORFM_DIR")
api_key = config.YOUTUBE_API


class Video:
    def __init__(self, id, name, date):
        self.id = id
        self.name = name
        self.date = date
        self.links: Links = None

    def get_tiny_urls(self, create: TinyURLAPI, short_name: str, tags: str = [""]):
        self.links["youtube"] = create.get_or_create_alias_url(
            f"https://youtu.be/{self.id}",
            f"{short_name}-YouTube",
            tags=tags.append("youtube"),
        )
        self.links["spotify"] = create.get_or_create_alias_url(
            self.links["spotify"],
            f"{short_name}-Spotify",
            tags=tags.append("spotify"),
        )
        self.links["apple"] = create.get_or_create_alias_url(
            self.links["apple"],
            f"{short_name}-Apple",
            tags=tags.append("apple"),
        )
        return f"""
*{self.name}*\n\n
*YouTube Link*\n\n{self.links['youtube']}\n
*Spotify Link*\n\n{self.links['spotify']}\n
*Apple Link*\n\n{self.links['apple']}
"""


def get_links(video: Video, show, show_name):
    video.links = get_episode_links(video.name, show, config)
    post = prepare_sharable_post(video.links, video.id, video.name)
    if any(value is None for value in video.links.values()):
        user_input = input("At least one value is None. Do you want to continue? (yes/no): ")
        if user_input.lower() != "yes":
            print(post)
            exit()

    creator = TinyURLAPI(config.TINY_URL_API_KEY)
    match show_name:
        case "pls":
            today = datetime.today()
            formatted_date = today.strftime("%m-%d")
            pls_l = video.get_tiny_urls(creator, "pls-" + formatted_date, tags=["pls"])
            print(video.name)
            print("\n")
            print(pls_l)

            pass
        case "gittin":
            digits = "".join([char for char in video.name if char.isdigit()])
            gittin_l = video.get_tiny_urls(creator, short_name=f"Gittin-{digits}", tags=["gittin"])
            print(gittin_l)
            print("\n")
            print("Short on time? Listen to a recap: ")
        case "halacha":
            today = datetime.today()
            formatted_date = today.strftime("%m-%d")

            halacha_l = video.get_tiny_urls(creator, "halacha-" + formatted_date)
            print(halacha_l)
        case "kolel":
            print(post)
        case "sg_chassidus":
            today = datetime.today()
            formatted_date = today.strftime("%m-%d")
            sg_chassidus_l = video.get_tiny_urls(creator, "chassidus-" + formatted_date)
            print(sg_chassidus_l)
        case "rm_torah":
            parsha = input("Enter the parsha: ")
            rm_torah_l = video.get_tiny_urls(creator, short_name=parsha, tags=["parsha"])
            print(rm_torah_l)
        case "rm_maamor":
            maamor = input("Enter the maamor: ")
            rm_maamor_l = video.get_tiny_urls(creator, short_name=f"maamorim-{maamor}", tags=["maamorim"])
            print(rm_maamor_l)


def get_all_videos_from_playlist(youtube, playlist_id):
    # Fetch all videos from the playlist
    videos = []
    nextPageToken = None
    try:
        while True:
            playlist_response = (
                youtube.playlistItems()
                .list(
                    part="snippet",
                    playlistId=playlist_id,
                    maxResults=50,
                    pageToken=nextPageToken,
                )
                .execute()
            )

            # Extract video details from the response
            for video in playlist_response["items"]:
                publish_time = video["snippet"]["publishedAt"]
                # convert date to datetime object
                publish_time_dt = datetime.strptime(publish_time, "%Y-%m-%dT%H:%M:%SZ")
                # convert from utc to est
                est_time = publish_time_dt.replace(tzinfo=timezone.utc).astimezone(ZoneInfo("America/New_York"))
                videos.append(
                    Video(
                        id=video["snippet"]["resourceId"]["videoId"],
                        name=video["snippet"]["title"],
                        date=est_time,
                    )
                )

            nextPageToken = playlist_response.get("nextPageToken")
            if not nextPageToken:
                break
    except googleapiclient.errors.HttpError as e:
        print(f"An error occurred: {e}")

    # Sort videos based on their published date in descending order
    # videos.sort(key=lambda x: x.date, reverse=True)

    return videos


def get_most_recent_videos_from_playlist(youtube, playlist_id, max_results):
    videos = []
    try:
        playlist_response = (
            youtube.playlistItems()
            .list(
                part="snippet",
                playlistId=playlist_id,
                maxResults=max_results,
            )
            .execute()
        )

        # Extract video details from the playlist_response
        for video in playlist_response["items"]:
            publish_time = video["snippet"]["publishedAt"]
            # convert date to datetime object
            publish_time_dt = datetime.strptime(publish_time, "%Y-%m-%dT%H:%M:%SZ")
            # convert from utc to est
            est_time = publish_time_dt.replace(tzinfo=timezone.utc).astimezone(ZoneInfo("America/New_York"))
            videos.append(
                Video(
                    id=video["snippet"]["resourceId"]["videoId"],
                    name=video["snippet"]["title"],
                    date=est_time,
                )
            )
    except googleapiclient.errors.HttpError as e:
        print(f"An error occurred: {e}")
    return videos


def get_video_metadata(youtube, video_id):
    try:
        video_response = (
            youtube.videos()
            .list(
                part="snippet",
                id=video_id,
            )
            .execute()
        )
        publish_time = video_response["items"][0]["snippet"]["publishedAt"]
        # convert date to datetime object()
        publish_time_dt = datetime.strptime(publish_time, "%Y-%m-%dT%H:%M:%SZ")
        # convert from utc to est_time
        est_time = publish_time_dt.replace(tzinfo=timezone.utc).astimezone(ZoneInfo("America/New_York"))
        return Video(
            id=video_id,
            name=video_response["items"][0]["snippet"]["title"],
            date=est_time,
        )
    except googleapiclient.errors.HttpError as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    show_names = [d for d in vars(config) if isinstance(vars(config)[d], dict)]
    print("Choose a Podcast show: ")
    for i, show in enumerate(show_names):
        print(f"{i}: {show}")

    show_num = int(input())
    shows = [vars(config)[d] for d in vars(config) if isinstance(vars(config)[d], dict)]

    # Specify the channel ID
    # channel_id = "UCU91spVc-WB73HnPZiEqMNQ"
    playlist_id = shows[show_num]["playlist_id"]

    # Set the number of results to be retrieved (max. 50)
    max_results = 15

    youtube = build("youtube", "v3", developerKey=api_key)
    # Create a YouTube API service object

    db = get_most_recent_videos_from_playlist(youtube, playlist_id, max_results)

    table = Table(title="Please choose from the following videos:")
    table.add_column("#", style="cyan", no_wrap=True)
    table.add_column("video ID", style="magenta")
    table.add_column("Date and Time", style="green")
    table.add_column("Name", style="cyan", no_wrap=True)

    for i, v in enumerate(db):
        table.add_row(str(i + 1), v.id, str(v.date), v.name)
        # print(i + 1, " | ", v.id, " | ", v.date, " | ", v.name)

    console = Console()
    console.print(table)

    choices = Prompt.ask(
        "Enter your choices separated by a comma: ",
        default="0",
        choices=[str(i) for i in range(len(db) + 1)],
    )

    choices = choices.split(",")

    for choice in choices:
        if choice == "0":
            # get video metadata
            video_id = input("Enter the video ID: ")
            print("Getting video metadata...")
            video = get_video_metadata(youtube, video_id)
            get_links(video, shows[show_num], show_names[show_num])
        else:
            get_links(db[int(choice) - 1], shows[show_num], show_names[show_num])
