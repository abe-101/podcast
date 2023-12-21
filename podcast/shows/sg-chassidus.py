import feedparser

import podcast.main as m

podcast = m.PodcastInfo(m.config.playlists[m.config.SG_CHASSIDUS])
title = "Mamor Bada Bishalom - Melukut 6 page 45"
short_name = "3-Chanukah-Maamar-Vol-2"


def get_short_links():
    title = feedparser.parse("https://feeds.captivate.fm/" + podcast.rss).entries[0].title
    links: m.podcast_links.Links = m.podcast_links.Links(title, short_name, podcast, m.config_manager)
    links.get_tiny_urls(["likutei-torah", "shloimy-greenwald"])
    print(links)
    links.send_whatsapp_msg()


if "__main__" == __name__:
    choice = input("1 - convert YouTube video, 2 - convert local file, 3 - get links: ")
    if choice == "1":
        url = input("Enter a YouTube URL: ")
        media: m.LocalMedia = m.download_yt.download_youtube_video(url, podcast.dir)
        episode = m.captivate_api.publish_podcast(local_media=media, podcast=podcast, config=m.config_manager)

        m.wait_with_progressbar(15 * 60)
        get_short_links()

    elif choice == "2":
        file = podcast.dir + "/" + title + ".m4a"
        file = m.adobe_podcast.enhance_podcast(file, m.config_manager)
        media: m.LocalMedia = m.LocalMedia(file_name=file, title=title, description=title)
        episode = m.captivate_api.publish_podcast(local_media=media, podcast=podcast, config=m.config_manager)

        video_pic = podcast.dir + "/" + podcast.name + ".jpg"
        media.file_name = m.audio_conversion.create_video_from_audio_and_picture(
            media.file_name, video_pic, podcast.dir + "/" + title + ".mp4"
        )
        media.keywords = (
            "chassidus, chassidut, chassidic, maamor, pada bishalom, badi bishalom, rabbi shloime greenwald, greenwald"
        )
        media: m.LocalMedia = m.upload_video.upload_video_with_options(
            media, privacyStatus="public", playlist_id=podcast.playlist_id, channel_id=podcast.channel_id
        )
        m.captivate_api.add_youtute_id_to_podcast(podcast, m.config_manager, media)
        print(media.url)

        m.wait_with_progressbar(8 * 60)
        get_short_links()

    elif choice == "3":
        get_short_links()

    elif choice == "4":
        previous = podcast.dir + "/" + "Chanukah Maamar Vol. 2, תנו רבנן- Part 1 (combined).mp3"
        new = podcast.dir + "/" + "Chanukah Maamar Vol. 2, תנו רבנן- Part 3.m4a"
        new = m.audio_conversion.convert_m4a_to_mp3(new)
        title = new.split("/")[-1].split(".")[0]
        episode_id = "02b94846-7b97-4296-bb1d-59b0d6da4131"

        m.add_audio_to_podcast(podcast, previous, new, episode_id)

        video_pic = podcast.dir + "/" + podcast.name + ".jpg"
        media: m.LocalMedia = m.LocalMedia(file_name=new, title=title, description=title)
        media.file_name = m.audio_conversion.create_video_from_audio_and_picture(
            new, video_pic, podcast.dir + "/" + title + ".mp4"
        )
        media: m.LocalMedia = m.upload_video.upload_video_with_options(
            media, privacyStatus="public", playlist_id=podcast.playlist_id, channel_id=podcast.channel_id
        )
