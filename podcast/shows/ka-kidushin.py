import os

import requests

from podcast.main import *  # NOQA: F401, F403

podcast = PodcastInfo(config.playlists[config.KA_KIDDUSHIN])  # NOQA: F405

# create_show_short_links(podcast)


def download_mp3(number):
    base_url = "http://download.kolavrohom.com/Kiddushin/"
    url = f"{base_url}{number}.mp3"
    output_filename = f"{podcast.dir}/{number}.mp3"

    response = requests.get(url)

    if response.status_code == 200:
        with open(output_filename, "wb") as file:
            file.write(response.content)
        print(f"File downloaded as '{output_filename}'")
        return os.path.abspath(output_filename)
    else:
        print("Failed to download the file.")
        return None


three = download_mp3("03")
title = "Kiddushin Daf 3 - Kol Avrohom Shas"
# file_to_captivate(podcast, three, title=title, artwork=podcast.dir + "/Kol-Avrohom.jpg", episode_num="3")
