import logging
import os
import time

from playwright.sync_api import Playwright, sync_playwright

from .audio_conversion import convert_wav_to_mp3
from .configuration_manager import ConfigurationManager


# Function to run the audio enhancement process using Adobe Podcast
def run(
    playwright: Playwright,
    file_name: str,
    config: ConfigurationManager,
    logger: logging.Logger = logging.getLogger(__name__),
) -> None:
    new_file = file_name.rsplit(".", 1)[0] + " (enhanced).mp3"
    # check if file was already enhanced
    if os.path.exists(new_file):
        print(f"file: {file_name}\n---\n   \\ was already enhanced, skipping")
        return new_file

    print(f"Enhancing file {file_name}")
    # Get the title of the file without the path
    title = file_name.rsplit("/", 1)[-1]
    # Launch the chromium browser
    browser = playwright.chromium.launch(headless=config.PLAYWRITE_HEADLESS)

    # Create a new context with saved authentication information
    # For first-time users, sign in manually and save the session and cookies using the command:
    # playwright codegen --save-storage=auth.json https://podcast.adobe.com/enhance#
    # More details:
    # https://playwright.dev/python/docs/cli#preserve-authenticated-state
    context = browser.new_context(storage_state="auth.json")
    page = context.new_page()
    # Go to the Adobe Podcast enhance page
    page.goto("https://podcast.adobe.com/enhance#")
    print("Waiting 5 sec for the page to load")
    time.sleep(5)

    # Wait for the page to load

    # Upload the audio file
    # page.get_by_label("Upload").set_input_files(file_name)
    # check if there is a div with title in it if yes download it
    # else upload the file
    title_selector = f'div > span[title="{title}"]'
    enhancing_text_selector = "text=Enhancing speech…"
    uploading_text_selector = "text=Uploading…"
    if page.query_selector(title_selector):
        print("File already uploaded")
        page.query_selector(title_selector).click()

    else:
        page.get_by_label("Choose files").set_input_files(file_name)
        print("Waiting for the file to be uploaded")
        # wait for button to be enabled

        # Wait for the file title to appear
        page.wait_for_selector(title_selector)
        time.sleep(5)

        print("Waiting for the file to be enhanced")
        count = 0
        while True:
            # Check if the "Enhancing speech…" text is still present on the page
            if not page.query_selector(enhancing_text_selector) and not page.query_selector(uploading_text_selector):
                time.sleep(5)
                page.wait_for_selector(title_selector).click()
                print("Enhancing done")
                break
            print(f"Still enhancing{'.' * (count % 4)}", end="\r")
            time.sleep(5)  # Wait for a few seconds before checking again
            count += 1

        # Now continuously check if "Enhancing speech" is still present with the file title
        # while True:
        #    # Find all elements that contain the text "Enhancing speech…"
        #    enhancing_elements = page.query_selector_all(enhancing_text_selector)
        #    # Check if any of these elements are associated with the file title
        #    is_enhancing = any(title in element.inner_text() for element in enhancing_elements)
        #    if not is_enhancing:
        #        page.wait_for_selector(title_selector).click()
        #        break

        #    time.sleep(5)  # Wait for a few seconds before checking again
        #    print("Still enhancing…")

        # selector = f'div.sc-bQlsKK.ceozLy.track-item > div > span[title="{title}"]'
        # page.wait_for_selector(selector, timeout=6000000).click()  # waits up to 60 seconds
        # print("Waiting for button to be enabled")

        # selector = f'div.sc-bQlsKK.hOcYTr.track-item > div > span[title="{title}"]'

        # page.wait_for_selector(selector, timeout=600000)  # waits up to 60 seconds
        # print("Waiting for button to be enabled")

    # Wait for the "Download" button to become available
    page.get_by_role("button", name="Download").wait_for(timeout=600000)

    print("Downloading the enhanced file")
    # Triggers the download of the enhanced file and gets its info
    with page.expect_download() as download_info:
        # Perform the action that initiates download
        page.get_by_role("button", name="Download").click()
    download = download_info.value
    # Waits for the download process to complete
    print(download.path())
    # Converts the enhanced audio from WAV to MP3 using FFmpeg
    print("doint the ffmpeg thing")
    new_name = convert_wav_to_mp3(download.path(), new_file)

    # ---------------------
    # Closes the context and browser instance
    context.close()
    browser.close()

    print(f"========\nSuccess!\n========\n\n{new_file}\n___\n   \\ has been enhanced!\n___/")
    return new_name


def enhance_podcast(
    file_name: str,
    config: ConfigurationManager,
    logger: logging.Logger = logging.getLogger(__name__),
) -> str:
    with sync_playwright() as playwright:
        new_file = run(playwright, file_name, config, logger)
    return new_file


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()

    config = ConfigurationManager()

    # Prompts the user for the audio file to enhance
    file_name = input("Which file would you like to enhance? ")
    new_file = enhance_podcast(file_name, config)
