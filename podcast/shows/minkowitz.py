from datetime import datetime

import feedparser

import podcast.main as m

mammorim: m.PodcastInfo = m.PodcastInfo(m.config.playlists[m.config.RM_MAAMOR])
torah: m.PodcastInfo = m.PodcastInfo(m.config.playlists[m.config.RM_TORAH])
zohar: m.PodcastInfo = m.PodcastInfo(m.config.playlists[m.config.RM_ZOHAR])

MAMMOR_ID = None
ZOHAR_ID = None

MAMMOR_ID = "_THvpXg5ILg"
MAMMOR_SHORT = "Creation-of-10-Sefirot"

# ZOHAR_ID = "Swg_Foy26C8"
ZOHAR_SHORT = "Zohar-Bereisheet"


if len(MAMMOR_SHORT) > 23 or len(ZOHAR_SHORT) > 23:
    raise ValueError("Short name is too long")


def youtube_to_captivatefm_publish_now(url: str, podcast: m.PodcastInfo):
    media: m.LocalMedia = m.download_yt.download_youtube_video(url, podcast.dir)
    media.upload_date = datetime.now()
    episode = m.captivate_api.publish_podcast(media, podcast, m.config_manager)
    return episode


if "__main__" == __name__:
    choice = input("What do you want to do? (1) create podcast, (2) generate links")
    if choice == "1":
        if MAMMOR_ID:
            youtube_to_captivatefm_publish_now(MAMMOR_ID, mammorim)
        if ZOHAR_ID:
            youtube_to_captivatefm_publish_now(ZOHAR_ID, zohar)

    elif choice == "2":
        if MAMMOR_ID:
            mammor_title = feedparser.parse("https://feeds.captivate.fm/" + mammorim.rss).entries[0].title
            mammor_links = m.podcast_links.Links(mammor_title, MAMMOR_SHORT, mammorim, m.config_manager)
            mammor_links.get_tiny_urls(["mammor"])
            mammor_links.send_whatsapp_msg()
            print(mammor_links.generate_template())

        if ZOHAR_ID:
            zohar_title = feedparser.parse("https://feeds.captivate.fm/" + zohar.rss).entries[0].title
            zohar_links = m.podcast_links.Links(zohar_title, ZOHAR_SHORT, zohar, m.config_manager)
            zohar_links.get_tiny_urls(["zohar"])
            zohar_links.send_whatsapp_msg()
            print(zohar_links.generate_template())
