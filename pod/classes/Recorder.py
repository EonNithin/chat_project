import subprocess
import os
import signal
from datetime import datetime
from django.conf import settings
import socket

# Define the base path for media files
media_folderpath = os.path.join(settings.BASE_DIR, 'media', 'processed_files')

class Recorder:
    def __init__(self):
        self.process = None
        self.device_name = None
        self.selected_subject = None
        self.filepath = None
        self.filename = None

    def start_recording(self, selected_subject):
        if self.process and self.process.poll() is None:
            print("Recording is already in progress.")
            return
        
        # Get the device name (hostname) and subject
        self.device_name = socket.gethostname()
        self.selected_subject = selected_subject

        # Generate filename with device name, timestamp, and subject
        timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        folder_name = f"{self.device_name}_{timestamp}_{self.selected_subject}"
        
        # Create a subdirectory with device name, timestamp, and subject inside media_folderpath
        self.filepath = os.path.join(media_folderpath, folder_name)
        os.makedirs(self.filepath, exist_ok=True)
        
        # Define the filename and the full file path
        self.filename = f"{self.device_name}_{timestamp}_{self.selected_subject}.mp4"
        self.filepath = os.path.join(self.filepath, self.filename)
        
        print(f"Saving to: {self.filepath}")

        # Define the FFmpeg command
        ffmpeg_cmd = [
            'ffmpeg', '-f', 'v4l2', '-i', '/dev/video2', '-c:v', 'libx264', '-crf', '18', self.filepath
        ]
        print("Running command:", ' '.join(ffmpeg_cmd))
        
        # Start the recording process
        self.process = subprocess.Popen(
            ffmpeg_cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=1,
            universal_newlines=True
        )
        
        # Capture and print the stderr for debugging
        stdout, stderr = self.process.communicate()
        print("FFmpeg output:", stdout)
        print("FFmpeg error output:", stderr)

        # self.process = subprocess.Popen(
        #     ['ffmpeg', '-i', 'rtsp://admin:hik@9753@192.168.0.252:554/Streaming/Channels/101', '-c:v', 'copy', self.filepath],
        #     stdin=subprocess.PIPE,
        #     stdout=subprocess.PIPE,
        #     stderr=subprocess.PIPE,
        #     bufsize=1,
        #     universal_newlines=True
        # )
        
        print(f"Recording started: {self.filename}, \n, {self.filepath}")

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
