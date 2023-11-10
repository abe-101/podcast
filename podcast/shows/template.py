import podcast.main as m

podcast = m.PodcastInfo(m.config.playlists[m.config.RM_MAAMOR])
title = ""

if "__main__" == __name__:
    choice = input("1 - convert YouTube video, 2 - convert local file, 3 - get links: ")
    if choice == "1":
        url = input("Enter a YouTube URL: ")
        media: m.LocalMedia = m.download_yt.download_youtube_video(url, podcast.dir)
        episode = m.captivate_api.publish_podcast(local_media=media, podcast=podcast, config=m.config_manager)

    elif choice == "2":
        file = input("Enter the file name: ")
        tile = file.split(".")[0]
        file = m.adobe_podcast.enhance_podcast(file, m.config_manager)
        media: m.LocalMedia = m.LocalMedia(file_name=file, title=title, description=title)
        episode = m.captivate_api.publish_podcast(local_media=media, podcast=podcast, config=m.config_manager)

        video_pic = podcast.dir + "/" + podcast.name + ".jpg"
        media.file_name = m.audio_conversion.create_video_from_audio_and_picture(
            media.file_name, video_pic, podcast.dir + "/" + title + ".mp4"
        )
        media: m.LocalMedia = m.upload_video.upload_video_with_options(
            media, privacyStatus="public", playlist_id=podcast.playlist_id, channel_id=podcast.channel_id
        )
        m.captivate_api.add_youtute_id_to_podcast(podcast, m.config_manager, media)
        print(media.url)

    elif choice == "3":
        title = m.podcast_links.choose_episode(podcast)
        short_name = input("Enter the short name of the podcast: ")
        links: m.podcast_links.Links = m.podcast_links.Links(title, podcast, m.config_manager)
        links.get_tiny_urls("short_name", [])
