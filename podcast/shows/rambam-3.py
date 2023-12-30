import feedparser
from imgurpython import ImgurClient

import podcast.main as m

podcast = m.PodcastInfo(m.config.playlists[m.config.RAMBAM_3])  # NOQA: F405
FIRST_PEREK = "Hilchos Gezelah Va'Avedah Perek 4"
SECOND_PEREK = "Hilchos Gezelah Va'Avedah Perek 5"
THIRD_PEREK = "Hilchos Gezelah Va'Avedah Perek 6"
TITLE = "Rambam: Hilchos Gezelah Va'Avedah Perek 4, 5, 6"
SHORT = "Gezala-4-5-6"


def number_to_hebrew(num):
    if num <= 0 or num > 200:
        raise ValueError("Number out of supported range")

    if num == 15:
        return "טו"
    if num == 16:
        return "טז"

    hebrew_numerals = {
        1: "א",
        2: "ב",
        3: "ג",
        4: "ד",
        5: "ה",
        6: "ו",
        7: "ז",
        8: "ח",
        9: "ט",
        10: "י",
        20: "כ",
        30: "ל",
        40: "מ",
        50: "נ",
        60: "ס",
        70: "ע",
        80: "פ",
        90: "צ",
        100: "ק",
        200: "ר",
    }

    result = []
    for value, letter in sorted(hebrew_numerals.items(), key=lambda x: x[0], reverse=True):
        while num >= value:
            result.append(letter)
            num -= value

    return "".join(result)


def get_title(daf_number):
    hebrew_daf = number_to_hebrew(daf_number)
    title = f"Bava Kamah Daf {daf_number} - מסכת בבא קמא דף {hebrew_daf} - Rabbi S Greenwald"
    return title


# file = podcast.dir + "/Kidushin Daf 8 - מסכת קידושין דף ח - Rabbi S Greenwald.mp3"


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


def get_short_links():
    title = feedparser.parse("https://feeds.captivate.fm/" + podcast.rss).entries[0].title
    # title = m.podcast_links.choose_episode(podcast)
    links: m.podcast_links.Links = m.podcast_links.Links(title, f"{SHORT}", podcast, m.config_manager)
    # links.title = links.title[:-20]
    links.get_tiny_urls(["shloime-greenwald", "Bava-Kamah"])
    print(links)
    links.send_whatsapp_msg()


if "__main__" == __name__:
    choice = input("1 - convert local video, 2 - get links: ")
    if choice == "1":
        perek_1 = m.get_file_extension(podcast.dir, FIRST_PEREK)
        perek_1 = m.adobe_podcast.enhance_podcast(perek_1, m.config_manager)
        perek_2 = m.get_file_extension(podcast.dir, SECOND_PEREK)
        perek_2 = m.adobe_podcast.enhance_podcast(perek_2, m.config_manager)
        perek_3 = m.get_file_extension(podcast.dir, THIRD_PEREK)
        perek_3 = m.adobe_podcast.enhance_podcast(perek_3, m.config_manager)

        combined = m.audio_conversion.combine_mp3_files(perek_1, perek_2, perek_3, podcast.dir + "/" + TITLE + ".mp3")
        title = TITLE

        description = f"""
{title}
"""  # NOQA: E231, E241
        media: m.LocalMedia = m.LocalMedia(file_name=combined, title=title, description=description)

        episode = m.captivate_api.publish_podcast(
            local_media=media,
            podcast=podcast,
            config=m.config_manager,
        )

        # video_pic = podcast.dir + "/youtube/00" + num_daf + ".png"
        # video_pic = podcast.dir + "/youtube/00.jpg"
        # media.file_name = m.audio_conversion.create_video_from_audio_and_picture(
        #     media.file_name, video_pic, podcast.dir + "/" + title + ".mp4"
        # )
        # media.keywords = f"Rambam, Rambam-3, Rab"  # NOQA: E231
        # media: m.LocalMedia = m.upload_video.upload_video_with_options(
        #     media, privacyStatus="public", playlist_id=podcast.playlist_id, channel_id=podcast.channel_id
        # )
        media.url = "https://youtu.be/9KhvQNAJr9M"
        m.captivate_api.add_youtute_id_to_podcast(podcast, m.config_manager, media)

        m.wait_with_progressbar(8 * 60)
        get_short_links()

    elif choice == "2":
        get_short_links()
