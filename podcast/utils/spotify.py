import time

import requests

from .configuration_manager import ConfigurationManager


def get_latest_spotify_episode_link(episode_name: str, podcast_channel_id: str, config: ConfigurationManager) -> str:
    """
    Retrieve the latest Spotify episode link for a given podcast channel
    and episode name using the provided access token.

    :param episode_name: The name of the episode to retrieve the link for.
    :type episode_name: str

    :param podcast_channel_id: The ID of the podcast channel to retrieve the link from.
    :type podcast_channel_id: str

    :param config: The config object with env secrets
    :type config: ConfigurationManager

    :return: The latest Spotify episode link for the given podcast channel and episode name.
    :rtype: str
    """
    access_token = config.get_spotify_token()
    count = 5
    while count > 0:
        url = f"https://api.spotify.com/v1/shows/{podcast_channel_id}/episodes?market=us"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers).json()

        episode = response["items"][0]
        if episode["name"] == episode_name:
            episode_link = episode["external_urls"]["spotify"]
            print(f"Found Spotify link for {episode_name}\n{episode_link}")
            return episode_link

        if len(response["items"]) < 5:
            shows_to_print = len(response["items"])
        else:
            shows_to_print = 5
        for i in range(shows_to_print):
            print(f'{i+1}. {response["items"][i]["name"]}')
        n = int(input("Choose episode 1-5 (0 to try again in 2): "))
        if n == 9:
            return None
        if n != 0:
            episode_link = response["items"][n - 1]["external_urls"]["spotify"]
            episode_name = response["items"][n - 1]["name"]
            print(f"Found Spotify link for {episode_name}\n{episode_link}")
            return episode_link

        print(f"episode: {episode_name} not yet found on {podcast_channel_id}")
        count -= 1
        print("waiting 2 minutes to try again")
        time.sleep(120)
