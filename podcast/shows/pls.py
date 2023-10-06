import time

import feedparser

import podcast.main as m

# m.config_manager.CAPTIVATE_USER_ID = "154d5721-ef7e-48b2-aebd-93e041fa5852"
# m.config_manager.CAPTIVATE_API_KEY = "AHs0ibbMoLxTRRWmUw18ygIJtKMRUJj8tjvWxhNF"

podcast = m.PodcastInfo(m.config.playlists[m.config.PLS])
short_name = "pls-24-brocha-1"


if "__main__" == __name__:
    choice = input("1 - convert YouTube video, 2 - convert local file, 3 - get links: 4 - add audio")
    if choice == "1":
        url = input("Enter a YouTube URL: ")
        media: m.LocalMedia = m.download_yt.download_youtube_video(url, podcast.dir)
        episode = m.captivate_api.publish_podcast(local_media=media, podcast=podcast, config=m.config_manager)

    elif choice == "2":
        # file = input("Enter the file name: ")
        file = podcast.dir + "/" + "Likkutei Sichos volume 24   Parshas Vsos Habracha - Rabbi Shloimy Greenwald.m4a"
        title = file.split("/")[-1].split(".")[0]
        file = m.adobe_podcast.enhance_podcast(file, m.config_manager)
        media: m.LocalMedia = m.LocalMedia(file_name=file, title=title, description=title)
        # episode = m.captivate_api.publish_podcast(local_media=media, podcast=podcast, config=m.config_manager)

        video_pic = podcast.dir + "/" + podcast.name + ".jpg"
        media.file_name = m.audio_conversion.create_video_from_audio_and_picture(
            media.file_name, video_pic, podcast.dir + "/" + title + ".mp4"
        )
        media: m.LocalMedia = m.upload_video.upload_video_with_options(
            media, privacyStatus="public", playlist_id=podcast.playlist_id, channel_id=podcast.channel_id
        )
        m.captivate_api.add_youtute_id_to_podcast(podcast, m.config_manager, media)

        print("Starting to wait...")
        time.sleep(15 * 60)  # 15 minutes in seconds
        print("Done waiting!")

        title = feedparser.parse("https://feeds.captivate.fm/" + podcast.rss).entries[0].title

        num_daf = "".join([char for char in title if char.isdigit()])
        links: m.podcast_links.Links = m.podcast_links.Links(title, short_name, podcast, m.config_manager)
        links.get_tiny_urls(["shloimy-greenwald", "pls"])
        links.send_whatsapp_msg()

    elif choice == "3":
        title = m.podcast_links.choose_episode(podcast)
        # short_name = input("Enter the short name of the podcast: ")
        links: m.podcast_links.Links = m.podcast_links.Links(title, short_name, podcast, m.config_manager)
        links.get_tiny_urls(["shloimy-greenwald", "pls"])
        links.send_whatsapp_msg()

    elif choice == "4":
        previous = (
            podcast.dir + "/"
            "Likkutei Sichos volume 24   Parshas Vsos Habracha - Rabbi Shloimy Greenwald (enhanced).mp3"
        )
        new = (
            podcast.dir
            + "/"
            + "Likkutei Sichos volume 24   Parshas Vsos Habracha - Rabbi Shloimy Greenwald - Part 2.mp3"
        )
        title = new.split("/")[-1].split(".")[0]
        new = m.adobe_podcast.enhance_podcast(new, m.config_manager)
        episode_id = "05207640-5a72-4b97-b198-7218f32594b1"

        m.add_audio_to_podcast(podcast, previous, new, episode_id)

        video_pic = podcast.dir + "/" + podcast.name + ".jpg"
        media: m.LocalMedia = m.LocalMedia(file_name=new, title=title, description=title)
        media.file_name = m.audio_conversion.create_video_from_audio_and_picture(
            new, video_pic, podcast.dir + "/" + title + ".mp4"
        )
        media: m.LocalMedia = m.upload_video.upload_video_with_options(
            media, privacyStatus="public", playlist_id=podcast.playlist_id, channel_id=podcast.channel_id
        )
