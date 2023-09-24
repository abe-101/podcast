import requests


def get_shows_apple_episode_links(apple_id: str) -> dict[str, str]:
    """
    Fetches the podcast episode names and their URLs from Apple Podcasts based on the given Apple ID.

    Parameters:
    - apple_id (str): The Apple ID of the podcast.

    Returns:
    - Dict[str, str]: A dictionary where the key is the episode's name and the value is its link.
    """
    if apple_id is None:
        return {}

    url = f"https://itunes.apple.com/lookup?id={apple_id}&country=US&media=podcast&entity=podcastEpisode"
    response = requests.get(url)
    data = response.json()

    episodes = {}

    # Looping from 1 because 0 contains metadata
    for result in data["results"][1:]:
        track_name = result.get("trackName", "")
        track_view_url = result.get("trackViewUrl", "")
        episodes[track_name] = track_view_url

    return episodes
