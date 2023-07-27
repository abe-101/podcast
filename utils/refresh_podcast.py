import csv

import feedparser
import yt_dlp
from configuration_manager import ConfigurationManager
from dotenv import load_dotenv

load_dotenv()
config = ConfigurationManager()
playlist_id = config.KOLEL_YOUTUBE_CHANNEL_ID
if playlist_id[:2] == "UC":
    playlist_id = "UU" + playlist_id[2:]
playlist_url = f"https://www.youtube.com/playlist?list={playlist_id}"

ydl_opts = {"dump_single_json": True, "extract_flat": True, "format": "best"}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    playlist_data = ydl.extract_info(playlist_url, download=False)

youtube = []
for entry in playlist_data["entries"]:
    youtube.append((entry["id"], entry["title"]))


url = "https://feeds.captivate.fm/" + config.kolel["rss"]
feed = feedparser.parse(url)
len(feed["entries"])

podcast_ids = set()

for entry in feed["entries"]:
    if entry["summary"][-4:] == "</p>":
        podcast_ids.add(entry["summary"][-15:-4])


len(podcast_ids)

podcast_titles = set()
for entry in feed["entries"]:
    podcast_titles.add(entry["title"])


def should_skip_title(title: str) -> bool:
    if "sota" in title.lower() or "sotah" in title.lower():
        return True
    if "kitzur" in title.lower() or "kittzur" in title.lower():
        return True
    if "קשו''ע" in title or "קיצור שו״ע" in title:
        return True
    if "sichos" in title.lower():
        return True
    if "greenwald" in title.lower():
        return True
    if (
        "סימן ק״ט" in title
        or "סימן קי״א" in title
        or "סימן ק״י" in title
        or "סימן ק״י ג" in title
        or "דיני החיטין" in title
    ):
        return True

    if "chassidic" in title.lower() or "hadrocho" in title.lower() or "communication" in title.lower():
        return True
    return False


needs_pod = []
for vid in youtube:
    if vid[0] not in podcast_ids and vid[1] not in podcast_titles and not should_skip_title(vid[1]):
        needs_pod.append(vid)


with open("needs_podcasts.csv", "w") as csvfile:
    writer = csv.writer(csvfile)
    for row in needs_pod:
        writer.writerow(row)
