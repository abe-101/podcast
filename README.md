# Podcast Automation Project

![Podcast Automation](https://github.com/abe-101/podcast/blob/main/podcast_automation.jpg)

## Overview

The Podcast Automation project is a Python-based tool that automates the process of creating podcasts from YouTube playlists. It provides a convenient way to download YouTube videos, convert them to MP3, enhance audio quality, and publish the resulting audio files as podcasts on Captivate.fm. The tool allows users to mimic given YouTube playlists and create corresponding podcasts effortlessly.

## Table of Contents

- [Project Description](#podcast-automation-project)
- [Table of Contents](#table-of-contents)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)

## Features

- Download YouTube videos and convert them to high-quality MP3 files.
- Enhance audio quality using an Adobe AI-powered tool (Playwright integration).
- Interact with the Captivate.fm API to upload and publish podcasts with metadata.
- Support for handling multiple YouTube playlists and their corresponding podcasts.
- Automatic generation of short URLs using the TinyURL API for easy sharing.
- Audio processing functions like normalizing volume, combining MP3 files, etc.

## Installation

1. Clone the project repository from GitHub:

   ```bash
   git clone https://github.com/abe-101/podcast.git
   ```

## Usage

The script will prompt you to select a playlist/podcast from the available options.
It will then fetch the 15 most recent videos from the selected YouTube playlist.
The videos will be converted into podcasts using audio enhancement.
The resulting podcasts will be uploaded and published on Captivate.fm with metadata.

## Configuration

The project uses a configuration file named `config.py` to store data for multiple playlists/podcasts. The configuration file includes information such as API keys, playlist IDs, directory paths, and URLs. You can modify this file to add, remove, or update playlist data as needed.

```python
PODCAST_1 = 0
PODCAST_2 = 1

playlists = [
    {
        "name": "podcast_1",
        "podcast_show_id": "<INSERT_CAPTIVATE_FM_SHOW_ID>",
        "spotify_id": "<INSERT_SHOWS_SPOTIFY_ID>",
        "dir": "<INSERT_DATA_DIR>",
        "apple_url": "<INSERT_SHOWS_APPLE_LINK>",
        "rss": "<INSERT_CAPTIVATE_FM_SHOW_RSS>",
        "playlist_id": "<INSERT_YOUTUBE_PLAYLIST_ID>",
        "google_url": "<INSERT_SHOWS_APPLE_LINK>",
        "channel_id": "<INSERT_YOUTUBE_CHANNEL_ID>",
    },
    {
        "name": "podcast_2",
        "podcast_show_id": "<INSERT_CAPTIVATE_FM_SHOW_ID>",
        "spotify_id": "<INSERT_SHOWS_SPOTIFY_ID>",
        "dir": "<INSERT_DATA_DIR>",
        "apple_url": "<INSERT_SHOWS_APPLE_LINK>",
        "rss": "<INSERT_CAPTIVATE_FM_SHOW_RSS>",
        "playlist_id": "<INSERT_YOUTUBE_PLAYLIST_ID>",
        "google_url": "<INSERT_SHOWS_APPLE_LINK>",
        "channel_id": "<INSERT_YOUTUBE_CHANNEL_ID>",
    },
]

YOUTUBE_API_KEY = "<INSERT_YOUTUBE_API_KEY>"
CAPTIVATE_USER_ID = "<INSERT_CAPTIVATE_FM_USER_ID>"
CAPTIVATE_API_KEY = "<INSERT_CAPTIVATE_FM_API_KEY>"
IMGUR_CLIENT_ID = "<INSERT_IMGUR_CLINET_ID>"
IMGUR_CLIENT_SECRET = "<INSERT_IMGUR_CLINET_SECRET>"
SPOTIFY_CLIENT_ID = "<INSERT_SPOTIFY_CLIENT_ID>"
SPOTIFY_CLIENT_SECRET = "<INSERT_SPOTIFY_CLIENT_SECRET>"
TINYURL_API_KEY = "<INSERT_TINY_URL_API_KEY>"
PLAYWRIGHT_HEADLESS = 'False'


```

## Dependencies

The project utilizes the following Python libraries:

- yt-dlp: For downloading YouTube videos and extracting metadata.
- Playwright: For interacting with the Adobe AI-powered audio enhancement tool.
- requests: For making HTTP requests to the Captivate.fm API and TinyURL API.
- Other standard Python libraries.

## Contributing

Contributions to the Podcast Automation project are welcome! If you find any bugs or want to add new features, please feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/abe-101/podcast/blob/main/LICENSE) file for details.

---

Happy Podcasting! 🎙️
