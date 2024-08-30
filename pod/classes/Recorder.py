import subprocess
import os
import signal
from datetime import datetime
from django.conf import settings

# Define the base path for media files
media_folderpath = os.path.join(settings.BASE_DIR, 'media', 'processed_files')

class Recorder:
    def __init__(self):
        self.process = None

    def start_recording(self):
        if self.process and self.process.poll() is None:
            print("Recording is already in progress.")
            return
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        filename = f"{timestamp}.mp4"
        filepath = f'{media_folderpath}/{filename}'

        self.process = subprocess.Popen(
            ['ffmpeg', '-i', 'rtsp://admin:hik@9753@192.168.0.252:554/Streaming/Channels/101', '-c:v', 'copy', filepath],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=1,
            universal_newlines=True
        )
        print(f"Recording started: {filename}, \n, {filepath}")

    def stop_recording(self):
        if self.process and self.process.poll() is None:
            self.process.stdin.write('q')
            self.process.stdin.flush()

            self.process.wait()
            print("Recording stopped.")
        else:
            print("No recording in progress.")

    def get_file_info(self):
        return {"filename": self.filename, "filepath": self.filepath}

    def __del__(self):
        if self.process and self.process.poll() is None:
            self.process.terminate()
            print("FFmpeg process terminated on deletion.")
