from datetime import date, timedelta

import feedparser
from imgurpython import ImgurClient

import podcast.main as m

podcast = m.PodcastInfo(m.config.playlists[m.config.SG_CHUMASH])  # NOQA: F405
PARSHA = "Shemos"


def get_thumbnail_link(parsha, num_day):
    try:
        client = ImgurClient(m.config.IMGUR_CLIENT_ID, m.config.IMGUR_CLIENT_SECRET)  # NOQA: F405
        pic = podcast.dir + "/podcast/" + parsha + ".jpg"
        uploaded_image = client.upload_from_path(pic)
        artwork = uploaded_image["link"]
        return artwork
    except Exception as e:
        print("Error occurred during image uploading:", str(e))


def get_chumash_text(num_day):
    """Gets the Chumash text for the specified day of the week.

    Args:
        num_day (int): The day of the week (0 for Monday, 6 for Sunday).

    Returns:
        str: The URL for the Chumash text for the specified day.
    """

    today = date.today()
    weekday = today.weekday()  # Get the current weekday (0-6)

    # Calculate the target date based on the given num_day
    target_weekday = (weekday + num_day) % 7
    target_date = today + timedelta(days=(target_weekday - weekday) + 1)

    # Format the date as mm/dd/yyyy
    formatted_date = target_date.strftime("%m/%d/%Y")

    chumash_text = f"https://www.chabad.org/dailystudy/torahreading.asp?tDate={formatted_date}"  # NOQA: E231

    return chumash_text


def get_short_links():
    title = feedparser.parse("https://feeds.captivate.fm/" + podcast.rss).entries[0].title
    num_day = "".join([char for char in title if char.isdigit()])
    links: m.podcast_links.Links = m.podcast_links.Links(title, f"{PARSHA}-{num_day}", podcast, m.config_manager)
    links.get_tiny_urls(["shloime-greenwald", "chumash"])
    chumash_link = get_chumash_text(num_day)
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
        + chumash_link
    )

    print(links.generate_template(template))

    # links.send_whatsapp_msg()


if "__main__" == __name__:
    choice = input("1 - convert YouTube video, 2 - convert local file, 3 - get links: ")
    if choice == "1":
        url = input("Enter a YouTube URL: ")
        media: m.LocalMedia = m.download_yt.download_youtube_video(url, podcast.dir)
        media.file_name = m.adobe_podcast.enhance_podcast(media.file_name, m.config_manager)
        num_day = "".join([char for char in media.title if char.isdigit()])
        media.thumbnail = get_thumbnail_link(PARSHA, num_day)

        episode = m.captivate_api.publish_podcast(local_media=media, podcast=podcast, config=m.config_manager)
        m.wait_with_progressbar(15 * 60)
        get_short_links()

    elif choice == "2":
        num_day = input("Enter the day of the week: ")
        file = m.get_file_extension(podcast.dir, f"{PARSHA}-{num_day}")
        print(file)
        title = f"Daily Chumash & Rashi: {PARSHA} - Portion {num_day}"
        was_m4a = m.audio_conversion.convert_m4a_to_mp3(file)
        print(was_m4a)
        if was_m4a:
            file = was_m4a
        file = m.adobe_podcast.enhance_podcast(file, m.config_manager)
        description = f"""
Dive into Portion {num_day} of {PARSHA} with Rabbi Shloimy Greenwald,

as we explore its teachings guided by the daily Chitas schedule.
"""  # NOQA: E231, E272
        media: m.LocalMedia = m.LocalMedia(file_name=file, title=title, description=description)
        media.thumbnail = get_thumbnail_link(PARSHA, num_day)

        episode = m.captivate_api.publish_podcast(local_media=media, podcast=podcast, config=m.config_manager)

        video_pic = f"{podcast.dir}/youtube/{PARSHA}.jpg"
        media.file_name = m.audio_conversion.create_video_from_audio_and_picture(
            media.file_name, video_pic, podcast.dir + "/" + title + ".mp4"
        )
        media: m.LocalMedia = m.upload_video.upload_video_with_options(
            media, privacyStatus="public", playlist_id=podcast.playlist_id, channel_id=podcast.channel_id
        )
        m.captivate_api.add_youtute_id_to_podcast(podcast, m.config_manager, media)

        m.wait_with_progressbar(8 * 60)
        get_short_links()

    elif choice == "3":
        get_short_links()
    elif choice == "4":
        youtube_id = input("Enter the YouTube ID: ")
        url = "https://youtu.be/" + youtube_id
        day_num = input("Enter the day of the week: ")
        short_url = f"{PARSHA}-{day_num}-YouTube"
        print(short_url)
        print(m.config_manager.TINY_URL_API_KEY)
        creator = m.tiny_url.TinyURLAPI(m.config_manager.TINY_URL_API_KEY)

        tiny_url = creator.get_or_create_alias_url(
            long_url=url, alias=short_url, tags=["shloime-greenwald", "chumash", "youtube"]
        )
        chumash_text = get_chumash_text(day_num)
        template = f"""
📖 Chumash & Rashi Shiur Alert! 📖

Join us tonight at 7:45 PM for a deep dive into this week's portion.

🔴 LIVE on YouTube 👉 {tiny_url}

Looking forward to seeing you all there! 📚🔍

Follow along at: {chumash_text}
"""  # NOQA: E231, E241, E203
        print(template)
