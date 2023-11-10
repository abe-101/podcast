import datetime
import os


def delete_old_files(directory_path):
    # Define the allowed file extensions
    allowed_extensions = [".mp3", ".m4a", ".mp4", ".wav", ".webm"]

    # Calculate the cutoff date (1 week ago)
    one_week_ago = datetime.datetime.now() - datetime.timedelta(days=7)

    # Walk through the directory tree
    for root, _, files in os.walk(directory_path):
        for filename in files:
            file_path = os.path.join(root, filename)

            # Check if the file has an allowed extension
            if any(file_path.lower().endswith(ext) for ext in allowed_extensions):
                # Get the file's modification time
                file_mtime = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))

                # Check if the file is older than one week
                if file_mtime < one_week_ago:
                    # Delete the file
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")


# Usage example:
directory_path = "data/"
delete_old_files(directory_path)
