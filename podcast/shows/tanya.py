from datetime import datetime

import feedparser
from imgurpython import ImgurClient
from pyluach import dates

import podcast.main as m

podcast = m.PodcastInfo(m.config.playlists[m.config.TANYA])  # NOQA: F405

MONTH = "כסלו"
TANYA_SEFER = "Likutei Amarim"

TEXT_URL = "https://www.chabad.org/dailystudy/tanya.asp?tdate="


def get_tanya_text(english_day_string, hebrew_date_url):
    date_object = datetime.strptime(english_day_string, "%Y-%m-%d")
    date = date_object.strftime("%m/%d/%Y")
    tanya_text = TEXT_URL + date

    creator = m.tiny_url.TinyURLAPI()
    tanya_link = creator.get_or_create_alias_url(
        long_url=tanya_text, alias=f"Tanya-{hebrew_date_url}-Text", tags=["shloime-greenwald", "tanya", "text"]
    )
    return tanya_link


def get_hebrew_date(english_day_string):
    date_object = datetime.strptime(english_day_string, "%Y-%m-%d")
    hebrew_date = dates.HebrewDate.from_pydate(date_object)
    return f"{hebrew_date: %*-d %*B}"


def get_hebrew_date_for_url(english_day_string):
    date_object = datetime.strptime(english_day_string, "%Y-%m-%d")
    hebrew_date = dates.HebrewDate.from_pydate(date_object)
    return f"{hebrew_date: %d-%B}"


def get_title(english_day_string, section):
    hebrew_date = get_hebrew_date(english_day_string)
    title = f"{TANYA_SEFER}, {section} - {hebrew_date}"
    return title


def get_thumbnail_link(num_daf):
    try:
        client = ImgurClient(m.config.IMGUR_CLIENT_ID, m.config.IMGUR_CLIENT_SECRET)  # NOQA: F405
        pic = podcast.dir + "/podcast/00" + num_daf + ".jpg"
        uploaded_image = client.upload_from_path(pic)
        artwork = uploaded_image["link"]
        return artwork
    except Exception as e:
        print("Error occurred during image uploading:", str(e))
        # Handle the error or take appropriate action here


def get_short_links(date):
    heb = get_hebrew_date(date)
    for entry in feedparser.parse("https://feeds.captivate.fm/" + podcast.rss).entries:
        if heb in entry.title:
            title = entry.title
            break
    # title = feedparser.parse("https://feeds.captivate.fm/" + podcast.rss).entries[0].title
    print(title)
    # title = m.podcast_links.choose_episode(podcast)
    hebrew_date_url = get_hebrew_date_for_url(date)
    links: m.podcast_links.Links = m.podcast_links.Links(title, f"Tanya-{hebrew_date_url}", podcast, m.config_manager)
    links.get_tiny_urls(["shloime-greenwald", "Tanya"])
    tanya_text = get_tanya_text(date, hebrew_date_url)
    print(links)
    template = (
        """
*{title}*

*YouTube Link*
{youtube}

*Spotify Link*
{spotify}

*Apple Link*
{apple}

*Text Link*
"""
        + tanya_text
    )
    print(links.generate_template(template))


if "__main__" == __name__:
    choice = input("1 - convert YouTube video, 2 - convert local file, 3 - get links: ")
    if choice == "1":
        url = input("Enter a YouTube URL: ")
        media: m.LocalMedia = m.download_yt.download_youtube_video(url, podcast.dir)
        media.file_name = m.adobe_podcast.enhance_podcast(media.file_name, m.config_manager)
        episode = m.captivate_api.publish_podcast(local_media=media, podcast=podcast, config=m.config_manager)

        # m.wait_with_progressbar(15 * 60)
        # get_short_links()

    elif choice == "2":
        date = input("Enter the date: ")  # 2020-11-30
        # file = podcast.dir + "/" + num_daf + ".m4a"
        file = m.get_file_extension(podcast.dir, date)
        title = input("Enter the title: ")
        title = get_title(date, title)
        print(title)
        # was_m4a = m.audio_conversion.convert_m4a_to_mp3(file)
        # print(was_m4a)
        # if was_m4a:
        #     file = was_m4a
        file = m.adobe_podcast.enhance_podcast(file, m.config_manager)
        hebrew_date_url = get_hebrew_date_for_url(date)
        description = f"""
{title}

Available on all major podcast platforms:
    https://My.Shiurim.net/Tanya-{hebrew_date_url}-Spotify
    https://My.Shiurim.net/Tanya-{hebrew_date_url}-YouTube
    https://My.Shiurim.net/Tanya-{hebrew_date_url}-Apple
"""  # NOQA: E231, E241

        print(description)
        media: m.LocalMedia = m.LocalMedia(file_name=file, title=title, description=description)
        # media.thumbnail = get_thumbnail_link(num_daf)
        episode = m.captivate_api.publish_podcast(local_media=media, podcast=podcast, config=m.config_manager)

        # video_pic = podcast.dir + "/youtube/00" + num_daf + ".png"
        video_pic = podcast.dir + "/youtube/00.jpg"
        media.file_name = m.audio_conversion.create_video_from_audio_and_picture(
            media.file_name, video_pic, podcast.dir + "/" + title + ".mp4"
        )
        media.keywords = f"tanya, {TANYA_SEFER}, {get_hebrew_date(date)}"
        media: m.LocalMedia = m.upload_video.upload_video_with_options(
            media, privacyStatus="public", playlist_id=podcast.playlist_id, channel_id=podcast.channel_id
        )
        m.captivate_api.add_youtute_id_to_podcast(podcast, m.config_manager, media)

        m.wait_with_progressbar(8 * 60)
        get_short_links(date)

    elif choice == "3":
        date = input("Enter the date: ")
        get_short_links(date)

    elif choice == "4":
        youtube_id = input("Enter the YouTube ID: ")
        url = "https://youtu.be/" + youtube_id
        daf_num = input("Enter the daf: ")
        short_url = f"Tanya-{daf_num}-YouTube"
        print(short_url)
        print(m.config_manager.TINY_URL_API_KEY)
        creator = m.tiny_url.TinyURLAPI(m.config_manager.TINY_URL_API_KEY)

        tiny_url = creator.get_or_create_alias_url(
            long_url=url, alias=short_url, tags=["shloime-greenwald", "bava-kamah", "youtube"]
        )
        template = f"""
🔔 Tonight's Gemorah Shiur Reminder! 🔔

Continuing our journey through Meseches Bava Kamah, we will be learning Daf g Daf g Daf g Daf g Daf g Daf g Daf g Daf g Daf g Daf g Daf g Daf g Daf {daf_num} tonight.

📅 Tonight Live at 8:15 PM:
📺 Join the *live* YouTube stream: {tiny_url}

Looking forward to seeing you all there! 📚🔍
"""  # NOQA: E231
        print(template)
