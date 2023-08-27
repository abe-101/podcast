from imgurpython import ImgurClient

import podcast.main as m

podcast = m.PodcastInfo(m.config.playlists[m.config.KIDUSHIN])  # NOQA: F405


def number_to_hebrew(num):
    if num <= 0 or num > 200:
        raise ValueError("Number out of supported range")

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
    title = f"Kidushin Daf {daf_number} - מסכת קידושין דף {hebrew_daf} - Rabbi S Greenwald"
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


if "__main__" == __name__:
    choice = input("1 - convert YouTube video, 2 - convert local file, 3 - get links: ")
    if choice == "1":
        url = input("Enter a YouTube URL: ")
        media: m.LocalMedia = m.download_yt.download_youtube_video(url, podcast.dir)
        num_daf = "".join([char for char in media.title if char.isdigit()])
        media.thumbnail = get_thumbnail_link(num_daf)
        episode = m.captivate_api.publish_podcast(
            local_media=media, podcast=podcast, config=m.config_manager, episode_num=str(num_daf)
        )

    elif choice == "2":
        num_daf = input("Enter the daf number: ")
        file = podcast.dir + "/" + num_daf + ".mp3"
        # title = file.split("/")[-1].split(".")[0]
        title = get_title(int(num_daf))
        file = m.adobe_podcast.enhance_podcast(file, m.config_manager)
        media: m.LocalMedia = m.LocalMedia(file_name=file, title=title, description=title)
        media.thumbnail = get_thumbnail_link(num_daf)
        episode = m.captivate_api.publish_podcast(
            local_media=media, podcast=podcast, config=m.config_manager, episode_num=str(num_daf)
        )

        video_pic = podcast.dir + "/YouTube/00" + num_daf + ".jpg"
        media.file_name = m.audio_conversion.create_video_from_audio_and_picture(
            media.file_name, video_pic, podcast.dir + "/" + title + ".mp4"
        )
        youtube_video = m.upload_video.upload_video_with_options(
            media, privacyStatus="public", playlist_id=podcast.playlist_id, channel_id=podcast.channel_id
        )
        media.url = youtube_video
        m.captivate_api.add_youtute_id_to_podcast(podcast, m.config_manager, media)
        print(youtube_video)

    elif choice == "3":
        title = m.podcast_links.choose_episode(podcast)
        num_daf = "".join([char for char in title if char.isdigit()])
        links: m.podcast_links.Links = m.podcast_links.Links(title, podcast, m.config_manager)
        links.get_tiny_urls(f"kidushin-{num_daf}", ["shloime-greenwald", "kidushin"])
        msg = f"""
*{links.title[:-20]}*
By Rabbi Shloimy Greenwald

*YouTube Link*

{links.youtube_short}

*Spotify Link*

{links.spotify_short}

*Apple Link*

{links.apple_short}
"""
        print(msg)
        print(links)
