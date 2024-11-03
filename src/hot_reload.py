import sys
import os
import time
import subprocess

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class ChangeHandler(FileSystemEventHandler):
    def __init__(self, app_process):
        super().__init__()
        self.app_process = app_process

    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            self.restart_application()

    def restart_application(self):
        if self.app_process:
            self.app_process.terminate()
            self.app_process.wait()

        self.app_process = subprocess.Popen([sys.executable, "src/main.py"])


def main():
    app_process = subprocess.Popen([sys.executable, "src/main.py"])

    path = os.path.dirname(os.path.abspath(__file__))

    event_handler = ChangeHandler(app_process)

    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        observer.stop()

    observer.join()

    if app_process:
        app_process.terminate()


if __name__ == "__main__":
    main()
