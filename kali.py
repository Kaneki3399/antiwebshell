import os
import time
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class FileEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return  # Ignore directory creation events (optional)

        # Check for desired file extensions (adjust as needed)
        if event.src_path.endswith(('.pdf', '.zip', '.exe', '.jpg', '.png')):
            file_path = event.src_path
            try:
                upload_time = os.path.getmtime(file_path)
                upload_datetime = datetime.fromtimestamp(upload_time)

                # Check if file creation time is recent (adjust threshold)
                is_recent = (time.time() - upload_time) < 60  # Downloaded within the last minute

                if is_recent:
                    print(f"Alert: New file possibly created!")
                    print(f"File Path: {file_path}")
                    print(f"Upload Time: {upload_datetime}")
                    print("-" * 120)
            except FileNotFoundError:
                print(f"Error: File not found yet: {file_path}")


def monitor_directories(directories):
    for directory in directories:
        event_handler = FileEventHandler()
        observer = Observer()
        observer.schedule(event_handler, path=directory, recursive=True)
        observer.start()
        print(f"Monitoring directory: {directory}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        for observer in observers:
            observer.stop()
        for observer in observers:
            observer.join()


if __name__ == "__main__":
    directories = [
        "/home",
        "/etc",
        "/var",  # Adjust directories to monitor as needed
    ]
    monitor_directories(directories)
