import logging
from datetime import datetime

import requests
from audio_conversion import normalize_volume
from configuration_manager import ConfigurationManager, LocalMedia


def format_date(date: datetime) -> str | None:
    """
    This function takes in a date string in the format "YYYYMMDD" and returns it in the format "YYYY-MM-DD 12:00:00"


    :param date_str: The date string to be formatted
    :type date_str: str
    :return: The formatted date string
    :rtype: Union[str, None]
    """
    try:
        formatted_date = date.strftime("%Y-%m-%d %H:%M:%S")
        return formatted_date

    except ValueError as e:
        print(e)
        return None


def upload_media(
    config: ConfigurationManager,
    show_id: str,
    file_name: str,
    logger: logging.Logger = logging.getLogger(__name__),
) -> str | None:
    """
    This function uploads a file to captivate.fm using an API, and returns the media_id.

    :param token: The API token to be used for authentication
    :type token: str
    :param show_id: The ID of the show's library you want your media to be uploaded in.
    :type show_id: str
    :param file_name: The name of the file to be uploaded
    :type file_name: str
    :return: The media_id of the uploaded file
    :rtype: Union[str, None]
    :raise: Exception if the file upload fails.
    """
    file_name = normalize_volume(file_name)
    token = config.get_captivate_token()
    headers = {
        "Authorization": "Bearer " + token,
    }

    files = {
        "file": open(
            file_name,
            "rb",
        ),
    }

    try:
        print(f"*~*Uploading {file_name} to captivate.fm")
        response = requests.post(
            f"https://api.captivate.fm/shows/{show_id}/media",
            headers=headers,
            files=files,
        )
        response.raise_for_status()
        r = response.json()
        return r["media"]["id"]
    except requests.exceptions.HTTPError as error:
        print(f"An HTTP error occurred: {error}")
        return None


def create_podcast(
    config: ConfigurationManager,
    title: str,
    media_id: str,
    date: str,
    shownotes: str,
    shows_id: str,
    episode_art: str = None,
    status: str = "Draft",
    episode_season: str = "1",
    episode_number: str = "1",
) -> str | None:
    """
    This function creates a podcast on captivate.fm using the API, by taking in all the parameters
    and putting them in the payload, and returns the response.

    :param token: The API token to be used for authentication
    :type token: str
    :param title: The title of the episode
    :type title: str
    :param media_id: The media_id of the episode
    :type media_id: str
    :param date: The date of the episode
    :type date: str
    :param shownotes: The shownotes of the episode
    :type shownotes: str
    :param shows_id: The id of the show
    :type shows_id: str
    :param status: The status of the episode
    :type status: str
    :param episode_season: The season of the episode
    :type episode_season: str
    :param episode_number: The number of the episode
    :type episode_number: str

    """
    token = config.get_captivate_token()
    url = "https://api.captivate.fm/episodes"

    payload = {
        "shows_id": shows_id,
        "title": title,
        "media_id": media_id,
        "date": date,
        "status": status,
        "shownotes": shownotes,
        "episode_season": episode_season,
        "episode_number": episode_number,
        "episode_art": episode_art,
    }

    files = []
    headers = {"Authorization": "Bearer " + token}

    try:
        print(f"*~* Creating {title} on captivate.fm")
        response = requests.request("POST", url, headers=headers, data=payload, files=files)
        response.raise_for_status()
        r = response.json()
        episode_id = r["record"]["id"]

        return f"https://player.captivate.fm/episode/{episode_id}"
    except requests.exceptions.HTTPError as error:
        print(f"An HTTP error occurred: {error}")
        return None


def get_episode(config: ConfigurationManager, episode_id: str) -> dict | None:
    """
    This function gets the full information for a episode

    :param token: The API token to be used for authentication
    :type token: str
    :param episode_id: The id of the episode
    :type file_name: str
    :return: a dict with the episode info
    :rtype: Union[dict, None]
    :raise: Exception if the file upload fails.
    """
    token = config.get_captivate_token()
    url = f"https://api.captivate.fm/episodes/{episode_id}"
    headers = {
        "Authorization": "Bearer " + token,
    }

    payload = {}

    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        response.raise_for_status()
        r = response.json()
        return r["episode"]
    except requests.exceptions.HTTPError as error:
        print(f"An HTTP error occurred: {error}")
        return None


def update_podcast(
    config: ConfigurationManager,
    media_id: str,
    shows_id: str,
    episode_id: str,
    shownotes: str,
    title: str,
    date: str,
    status: str = "draft",
    episode_season: str = "1",
    episode_number: str = "1",
) -> str | None:
    token = config.get_captivate_token()
    url = f"https://api.captivate.fm/episodes/{episode_id}"

    payload = {
        "shows_id": shows_id,
        "media_id": media_id,
        "title": title,
        "date": date,
        "status": status,
        "shownotes": shownotes,
        "episode_season": episode_season,
        "episode_number": episode_number,
    }

    files = []
    headers = {"Authorization": "Bearer " + token}

    try:
        print(f"*~* Updating {title} on captivate.fm")
        response = requests.request("PUT", url, headers=headers, data=payload, files=files)
        response.raise_for_status()
        r = response.json()
        episode_id = r["episode"]["id"]

        return f"https://player.captivate.fm/episode/{episode_id}"
    except requests.exceptions.HTTPError as error:
        print(f"An HTTP error occurred: {error}")
        return None


def publish_podcast(
    local_media: LocalMedia,
    show: dict[str, str],
    config: ConfigurationManager,
    episode_num: str = "1",
    logger: logging.Logger = logging.getLogger(__name__),
) -> str:
    """
    Publishes an audio file as a new podcast episode on CaptivateFM.

    Args:
        info: A dictionary containing information about the podcast episode.
            Required keys: "upload_date", "file_name", "title", "description", "url".
        show: A dictionary containing information about the show.
            Required keys: "show_id".

    Returns:
        The URL of the newly published podcast episode.

    Raises:
        ValueError: If any required keys are missing from the info or show dictionaries.
    """
    formatted_upload_date = format_date(local_media.upload_date)
    show_id = show["show_id"]
    media_id = upload_media(config=config, show_id=show_id, file_name=local_media.file_name)

    video_id = local_media.url[-11:]
    short_youtube_url = "youtu.be/" + video_id
    youtube = "\nWatch on YouTube: <a href='" + local_media.url + "'>" + short_youtube_url + "</a>\n"
    brought_by = """
\nBrought to you by: <b><a href='https://www.shiurim.net/'>Shiurim.net</a></b>
Contact us for all your podcast needs: <a href='mailto:podcast@shiurim.net'>podcast@shiurim.net</a>\n
    """
    shownotes = local_media.description + youtube + brought_by
    episode_id = create_podcast(
        config=config,
        media_id=media_id,
        date=formatted_upload_date,
        title=local_media.title,
        shownotes=shownotes,
        shows_id=show_id,
        episode_number=episode_num,
        episode_art=local_media.thumbnail,
    )
    return episode_id
