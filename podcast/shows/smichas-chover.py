import podcast.main as m

TOPIC = "niddah"
DIR = "data/smichas-chover"


if "__main__" == __name__:
    choice = input("1 - enhnace audio: ")
    num = input("Enter number lecture: ")
    file = m.get_file_extension(DIR, f"{TOPIC}-{num}")
    print(file)
    file = m.adobe_podcast.enhance_podcast(file, m.config_manager)
    print(file)
