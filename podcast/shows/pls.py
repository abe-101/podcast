import feedparser

import podcast.main as m

# m.config_manager.CAPTIVATE_USER_ID = "154d5721-ef7e-48b2-aebd-93e041fa5852"
# m.config_manager.CAPTIVATE_API_KEY = "AHs0ibbMoLxTRRWmUw18ygIJtKMRUJj8tjvWxhNF"

podcast = m.PodcastInfo(m.config.playlists[m.config.PLS])
short_name = "3-pls-15-10-Teves"


def get_short_links():
    title = feedparser.parse("https://feeds.captivate.fm/" + podcast.rss).entries[0].title
    links: m.podcast_links.Links = m.podcast_links.Links(title, short_name, podcast, m.config_manager)
    links.get_tiny_urls(["shloimy-greenwald", "pls"])
    print(links)
    template = """
*{title}*

*YouTube Link*
{youtube}

*Spotify Link*
{spotify}
{apple}
"""
    print(links.generate_template(template))

    links.send_whatsapp_msg()


if "__main__" == __name__:
    choice = input("1 - convert YouTube video, 2 - convert local file, 3 - get links: 4 - add audio")
    if choice == "1":
        url = input("Enter a YouTube URL: ")
        media: m.LocalMedia = m.download_yt.download_youtube_video(url, podcast.dir)
        # media.file_name = m.adobe_podcast.enhance_podcast(media.file_name, m.config_manager)
        episode = m.captivate_api.publish_podcast(local_media=media, podcast=podcast, config=m.config_manager)

    elif choice == "2":
        # file = input("Enter the file name: ")
        file = podcast.dir + "/" + "Likkutei Sichos | Volume 15 | 10h of Teves.m4a"
        title = file.split("/")[-1].split(".")[0]
        file = m.adobe_podcast.enhance_podcast(file, m.config_manager)
        media: m.LocalMedia = m.LocalMedia(file_name=file, title=title, description=title)
        episode = m.captivate_api.publish_podcast(local_media=media, podcast=podcast, config=m.config_manager)

        video_pic = podcast.dir + "/" + podcast.name + ".jpg"
        media.keywords = (
            f"{short_name}, pls, project likutei sichos, Likkutei Sichos" "volume 15, 10th of teves, greenwald"
        )

        media.file_name = m.audio_conversion.create_video_from_audio_and_picture(
            media.file_name, video_pic, podcast.dir + "/" + title + ".mp4"
        )
        media: m.LocalMedia = m.upload_video.upload_video_with_options(
            media, privacyStatus="public", playlist_id=podcast.playlist_id, channel_id=podcast.channel_id
        )
        m.captivate_api.add_youtute_id_to_podcast(podcast, m.config_manager, media)

        m.wait_with_progressbar(15 * 60)
        get_short_links()

    elif choice == "3":
        get_short_links()

    elif choice == "4":
        previous = podcast.dir + "/" + "Likkutei Sichos | Volume 15 | 10h of Teves (enhanced) (combined).mp3"
        new = podcast.dir + "/" + "Part 3: Likkutei Sichos | Volume 15 | 10h of Teves.mp3"
        title = new.split("/")[-1].split(".")[0]
        # url = "kgcfZfxdwj0"
        # media: m.LocalMedia = m.download_yt.download_youtube_video(url, podcast.dir)
        # new = m.adobe_podcast.enhance_podcast(media.file_name, m.config_manager)
        # new = media.file_name
        new = m.adobe_podcast.enhance_podcast(new, m.config_manager)
        episode_id = "4ec3e362-7b95-40fd-b214-233e4f88212e"

        m.add_audio_to_podcast(podcast, previous, new, episode_id)

        video_pic = podcast.dir + "/" + podcast.name + ".jpg"
        media: m.LocalMedia = m.LocalMedia(file_name=new, title=title, description=title)
        media.keywords = (
            f"{short_name}, pls, project likutei sichos, Likkutei Sichos"
            "volume 15, toldos, sichah 5, part 3, greenwald"
        )
        media.file_name = m.audio_conversion.create_video_from_audio_and_picture(
            new, video_pic, podcast.dir + "/" + title + ".mp4"
        )
        media: m.LocalMedia = m.upload_video.upload_video_with_options(
            media, privacyStatus="public", playlist_id=podcast.playlist_id, channel_id=podcast.channel_id
        )
    elif choice == "5":
        youtube_id = input("Enter the YouTube ID: ")
        url = "https://youtu.be/" + youtube_id
        creator = m.tiny_url.TinyURLAPI(m.config_manager.TINY_URL_API_KEY)

        tiny_url = creator.get_or_create_alias_url(
            long_url=url, alias=short_name + "-YouTube", tags=["shloime-greenwald", "pls", "youtube"]
        )
        print(tiny_url)
