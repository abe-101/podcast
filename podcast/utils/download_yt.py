# from gevent import monkey
# monkey.patch_all()

import logging
import os
import unicodedata
from http.client import IncompleteRead

from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError

from .configuration_manager import LocalMedia


def clean_video_title(title):
    cleaned_title = unicodedata.normalize("NFKC", title)
    return cleaned_title.strip()


def download_youtube_video(
    url: str,
    folder_path: str,
    logger: logging.Logger = logging.getLogger(__name__),
) -> dict[str, str]:
    """
    This function downloads a YouTube video from the given URL, and returns a dictionary
    containing the video's title, description, file name and upload date.

    :param url: The URL of the YouTube video to download
    :type url: str
    :param folder_path: The folder on disk where to download and save the audio
    :type folder_path: str
    :return: A dictionary containing the video's title, description, file name, and upload date
    :rtype: Dict[str, str]
    """
    with YoutubeDL(
        {
            "format": "bestaudio/best",
            "outtmpl": f"{folder_path}/%(id)s.%(ext)s",
            "keepvideo": True,
            "live_from_start": True,
            # 'concurrent_fragment_downloads': 4,
            "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3"}],
            "no_windows_filenames": True,
        }
    ) as ydl:
        retry_count = 0
        max_retries = 3
        while retry_count < max_retries:
            try:
                video_info = ydl.extract_info(url, download=False)  # Extract metadata without downloading
                break  # Break the loop if extraction succeeds
            except (DownloadError, IncompleteRead) as e:
                retry_count += 1
                print(f"Metadata extraction attempt {retry_count} failed with error: {e}. Retrying...")
        else:
            print(f"Failed to extract metadata after {max_retries} attempts.")
            return None

        file_name = f"{folder_path}/{video_info['title']}.mp3"  # Get the file name based on the video title

        if os.path.exists(file_name):
            print("Video already exists. Skipping download.")
        else:
            retry_count = 0
            while retry_count < max_retries:
                try:
                    ydl.download([url])  # Download the video
                    os.rename(
                        f'{folder_path}/{video_info["id"]}.mp3', file_name
                    )  # Rename the file to match the video title
                    break  # Break the loop if download succeeds
                except DownloadError as e:
                    retry_count += 1
                    print(f"Download attempt {retry_count} failed with error: {e}. Retrying...")
            else:
                print(f"Failed to download the video after {max_retries} attempts.")
                return None

    if len(url) == 11:
        url = f"https://www.youtube.com/watch?v={url}"

    local_media = LocalMedia(
        file_name=file_name,
        title=video_info["title"],
        description=video_info.get("description"),
        url=url,
        thumbnail=video_info.get("thumbnail"),
    )
    # local_media.set_upload_date_from_timestamp(video_info.get("release_timestamp"))
    # if local_media.upload_date is None or local_media.upload_date == "":
    local_media.set_upload_date_from_string(video_info.get("upload_date"))
    return local_media
