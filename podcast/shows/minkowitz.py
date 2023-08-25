from datetime import datetime

import feedparser

import podcast.main as m

mammorim: m.PodcastInfo = m.PodcastInfo(m.config.playlists[m.config.RM_MAAMOR])
torah: m.PodcastInfo = m.PodcastInfo(m.config.playlists[m.config.RM_TORAH])

MAMMOR_ID = "a-xUwspKOSw"
MAMMOR_SHORT = "Spiritual-First-Fruits"
TORAH_ID = "Js8mso64hQo"
TORAH_SHORT = "Ki-Tavo"


def youtube_to_captivatefm_publish_now(url: str, podcast: m.PodcastInfo):
    media: m.LocalMedia = m.download_yt.download_youtube_video(url, podcast.dir)
    media.upload_date = datetime.now()
    episode = m.captivate_api.publish_podcast(media, podcast, m.config_manager)
    return episode


if "__main__" == __name__:
    choice = input("What do you want to do? (1) create podcast, (2) generate links")
    if choice == "1":
        youtube_to_captivatefm_publish_now(TORAH_ID, torah)
        youtube_to_captivatefm_publish_now(MAMMOR_ID, mammorim)

    elif choice == "2":
        maamor_title = feedparser.parse("https://feeds.captivate.fm/" + mammorim.rss).entries[0].title
        torah_title = feedparser.parse("https://feeds.captivate.fm/" + torah.rss).entries[0].title

        maamor_links = m.podcast_links.Links(maamor_title, mammorim, m.config_manager)
        maamor_links.get_tiny_urls(MAMMOR_SHORT, ["maamor"])

        torah_links = m.podcast_links.Links(torah_title, torah, m.config_manager)
        torah_links.get_tiny_urls(TORAH_SHORT, ["torah"])

        print(maamor_links.whatsapp_str())
        print(torah_links.whatsapp_str())
