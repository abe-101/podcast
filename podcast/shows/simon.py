import csv
import os
import re
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

import feedparser
import googleapiclient.errors
from googleapiclient.discovery import build

import podcast.main as m

api_key = m.config.YOUTUBE_API_KEY


class Video:
    def __init__(self, id, name, date):
        self.id = id
        self.name = name
        self.date = date
        # self.links: Links = None


def get_new_videos(podcast: m.PodcastInfo):
    playlist_id = podcast.playlist_id

    # max_results = 49

    youtube = build("youtube", "v3", developerKey=api_key)
    # Create a YouTube API service object

    # db = get_most_recent_videos_from_playlist(youtube, playlist_id, max_results)
    if not os.path.exists(f"{playlist_id}.csv"):
        db = get_all_videos_from_playlist(youtube, playlist_id)
        with open(f"{playlist_id}.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "name", "date"])
            for video in db:
                writer.writerow([video.id, video.name, video.date])
    else:
        db = []
        with open(f"{playlist_id}.csv") as f:
            reader = csv.reader(f)
            for row in reader:
                db.append(Video(row[0], row[1], row[2]))

    # playlist_url = f"https://www.youtube.com/playlist?list={show['playlist_id']}"
    # ydl_opts = {"dump_single_json": True, "extract_flat": True, "format": "best"}
    #
    # with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    #    playlist_data = ydl.extract_info(playlist_url, download=False)

    podcast_ids = set()
    podcast_titles = set()

    url = "https://feeds.captivate.fm/" + podcast.rss
    feed = feedparser.parse(url)
    print(len(feed["entries"]))

    for entry in feed["entries"]:
        youutbe_id = find_youtube_video_id(entry["summary"])
        if youutbe_id:
            podcast_ids.add(youutbe_id)
        podcast_titles.add(entry["title"])
    print(f"Podcast ids: {len(podcast_ids)}")
    print(f"Podcast titles: {len(podcast_titles)}")

    youtube = []
    db.sort(key=lambda x: x.date)
    for video in db:
        if video.id not in podcast_ids and video.name not in podcast_titles:
            youtube.append((video.id, video.name))

    print(f"Youtube: {len(youtube)}")
    # ensure there are no duplicates
    youtube = list(set(youtube))
    print(f"Youtube: {len(youtube)}")
    return youtube


def find_youtube_video_id(text):
    pattern = r"(?:youtube\.com\/watch\?v=|youtu.be\/)([A-Za-z0-9_-]+)"
    match = re.search(pattern, text)
    if match:
        video_id = match.group(1)
        return video_id
    else:
        return None


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
                    Video(id=video["snippet"]["resourceId"]["videoId"], name=video["snippet"]["title"], date=est_time)
                )

            nextPageToken = playlist_response.get("nextPageToken")
            if not nextPageToken:
                break
    except googleapiclient.errors.HttpError as e:
        print(f"An error occurred: {e}")

    # Sort videos based on their published date in descending order
    videos.sort(key=lambda x: x.date)

    return videos


podcast = m.PodcastInfo(m.config.playlists[m.config.SIMON])

SHORT_NAME = "Soul-of-Yom-Kippur"
YOU_TUBE_ID = "x57R3pkUigM"

if "__main__" == __name__:
    choice = input("1 - convert YouTube video, 2 - get links: ")
    if choice == "1":
        url = YOU_TUBE_ID
        media: m.LocalMedia = m.download_yt.download_youtube_video(url, podcast.dir)
        episode = m.captivate_api.publish_podcast(local_media=media, podcast=podcast, config=m.config_manager)

    if choice == "2":
        title = feedparser.parse("https://feeds.captivate.fm/" + podcast.rss).entries[0].title
        short_name = SHORT_NAME
        links: m.podcast_links.Links = m.podcast_links.Links(title, short_name, podcast, m.config_manager)
        links.get_tiny_urls(["simon"])
        links.send_whatsapp_msg()

    if choice == "3":
        youtube = get_new_videos(podcast)
        n = len(youtube)
        count = 1
        for id, title in youtube:
            print(f"Downloading:{count}/{n} - {title}")
            media: m.LocalMedia = m.download_yt.download_youtube_video(id, podcast.dir)
            episode = m.captivate_api.publish_podcast(
                local_media=media, podcast=podcast, config=m.config_manager, episode_num=1
            )
            count += 1
