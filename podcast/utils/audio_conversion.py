import os

from moviepy.editor import AudioFileClip, ImageClip
from pydub import AudioSegment


def normalize_volume(file_path: str, target_dBFS: float = -15.0) -> str:
    sound = AudioSegment.from_mp3(file_path)
    change_in_dBFS = target_dBFS - sound.dBFS
    normalized_sound = sound.apply_gain(change_in_dBFS)

    # Export the normalized sound and overwrite the original file
    normalized_sound.export(file_path, format="mp3")

    # Print the process
    print(f"Normalized volume of '{file_path}' to {target_dBFS} dBFS.")
    print(f"Overwrote the original file '{file_path}' with the normalized audio.")

    return file_path


def convert_m4a_to_mp3(file_name: str) -> None | str:
    """
    Convert a given .m4a file to .mp3 format.

    Args:
    - file_name (str): The name of the file to be converted.

    Returns:
    - str: The name of the converted file if the input file was m4a.
    - None: If the input file wasn't an m4a file.
    """

    if file_name.lower().endswith(".m4a"):
        audio = AudioSegment.from_file(file_name, "m4a")

        mp3_file_name = file_name.rsplit(".", 1)[0] + ".mp3"
        audio.export(mp3_file_name, format="mp3")

        return mp3_file_name

    return None


def create_video_from_audio_and_picture(audio_path: str, image_path: str, output_path: str) -> str:
    """Create and save a video file to `output_path` after
    combining a static image that is located in `image_path`
    with an audio file in `audio_path`
    https://www.thepythoncode.com/article/add-static-image-to-audio-in-python
    """
    if os.path.exists(output_path):
        print(f"file: {output_path}\n---\n   \\ was already created, skipping")
        return output_path

    # create the audio clip object
    audio_clip = AudioFileClip(audio_path)
    # create the image clip object
    image_clip = ImageClip(image_path)
    # use set_audio method from image clip to combine the audio with the image
    video_clip = image_clip.set_audio(audio_clip)
    # specify the duration of the new clip to be the duration of the audio clip
    video_clip.duration = audio_clip.duration
    # set the FPS to 1
    video_clip.fps = 1
    # write the resuling video clip
    video_clip.write_videofile(output_path)
    return output_path


def convert_wav_to_mp3(input_file: str, output_file: str | None = None) -> str:
    """Convert WAV audio file to MP3.

    :param input_file: The file path of the WAV audio file to be converted.
    :type input_file: str
    :param output_file: The file path where the MP3 file will be saved. If not provided,
    the original file name will be used, with the '.wav' extension changed to '.mp3'.
    :type output_file: Optional[str], optional
    :return: The file path of the MP3 file.
    :rtype: str
    """
    if not output_file:
        output_file = input_file.rsplit(".", 1)[0] + ".mp3"

    sound = AudioSegment.from_wav(input_file)
    sound.export(output_file, format="mp3")

    return output_file


def combine_mp3_files(file1: str, file2: str) -> str:
    """Combine two mp3 files into one.

    :param file1: The path to the first mp3 file.
    :type file1: str
    :param file2: The path to the second mp3 file.
    :type file2: str
    :return: The combined audio.
    :rtype: AudioSegment
    """
    sound1 = AudioSegment.from_mp3(file1)
    sound2 = AudioSegment.from_mp3(file2)
    combined = sound1 + sound2
    new = file1.rsplit(".", 1)[0] + " (combined).mp3"
    combined.export(new, format="mp3")
    return new


def combine_m4a_files(file1: str, file2: str) -> str:
    """Combine two m4a files into one.

    :param file1: The path to the first m4a file.
    :type file1: str
    :param file2: The path to the second m4a file.
    :type file2: str
    :return: The combined audio.
    :rtype: AudioSegment
    """
    sound1 = AudioSegment.from_file(file1, format="m4a")
    sound2 = AudioSegment.from_file(file2, format="m4a")
    combined = sound1 + sound2
    new = file1.rsplit(".", 1)[0] + " (combined).mp3"
    combined.export(new, format="mp3")
    return new


def combine_webm_files(input_file1: str, input_file2: str, output_file: str = None) -> None:
    """
    Combine two WebM audio files into a single file.

    :param input_file1: Path to the first WebM audio file to combine.
    :type input_file1: str
    :param input_file2: Path to the second WebM audio file to combine.
    :type input_file2: str
    :param output_file: Path to the output audio file.
    :type output_file: str
    """
    # Load the input files using Pydub.
    sound1 = AudioSegment.from_file(input_file1, format="webm")
    sound2 = AudioSegment.from_file(input_file2, format="webm")

    # Combine the two audio segments using Pydub.
    combined_sound = sound1 + sound2

    if output_file is None:
        output_file = input_file1.rsplit(".", 1)[0] + " (combined).webm"

    # Export the combined audio as a WebM file using Pydub.
    combined_sound.export(output_file, format="webm")
    return output_file
