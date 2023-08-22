# podcast_info.py


class PodcastInfo:
    def __init__(self, data: dict):
        self.name: str = data.get("name", "")
        self.podcast_show_id: str = data.get("podcast_show_id", "")
        self.spotify_id: str = data.get("spotify_id", "")
        self.dir: str = data.get("dir", "")
        self.apple_url: str = data.get("apple_url", "")
        self.rss: str = data.get("rss", "")
        self.playlist_id: str = data.get("playlist_id", "")
        self.google_url: str | None = data.get("google_url", None)
