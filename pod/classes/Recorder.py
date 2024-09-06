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
       self.streaming_process = None
       self.grab_process = None
       self.stream_port = 8090  # You can choose a different port if needed
       self.timestamp = None
       
   def update_timestamp(self):
       self.timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
       #self.timestamp = "test"

   def start_recording(self):
       self.update_timestamp()
       if self.process and self.process.poll() is None:
           print("Recording is already in progress.")
           return

       # Create a subdirectory with the timestamp inside media_folderpath
       self.filepath = os.path.join(media_folderpath, self.timestamp)
       os.makedirs(self.filepath, exist_ok=True)
       # Define the filename and the full file path
       self.filename = f"{self.timestamp}_recorded_video.mp4"
       self.filepath = os.path.join(self.filepath, self.filename)


       self.process = subprocess.Popen(
           ['ffmpeg', '-i', 'rtsp://admin:hik@9753@192.168.0.252:554/Streaming/Channels/101', '-c:v', 'copy', self.filepath],
           stdin=subprocess.PIPE,
           stdout=subprocess.PIPE,
           stderr=subprocess.PIPE,
           bufsize=1,
           universal_newlines=True
       )
       print(f"Recording started: {self.filename}, \n, {self.filepath}")
       
      
   def start_screen_grab(self):
       if self.grab_process and self.grab_process.poll() is None:
           print("Grab is already in progress.")
           return

       # Create a subdirectory with the timestamp inside media_folderpath
       self.grabpath = os.path.join(media_folderpath, self.timestamp)
       os.makedirs(self.grabpath, exist_ok=True)
       # Define the filename and the full file path
       self.filename = f"{self.timestamp}_screen_grab.mp4"
       self.filepath = os.path.join(self.grabpath, self.filename)
       
       self.grab_process = subprocess.Popen(
           ['ffmpeg', '-thread_queue_size', '1024', '-i', '/dev/video0' ,'-r', '30', '-c:v', 'h264_rkmpp', '-preset medium', '-crf', '21', self.filepath],
           stdin=subprocess.PIPE,
           stdout=subprocess.PIPE,
           stderr=subprocess.PIPE,
           bufsize=1,
           universal_newlines=True
       )
       print(f"Screen Grab started: {self.filename}, \n, {self.filepath}")


   def stop_recording(self):
       if self.process and self.process.poll() is None:
           self.process.stdin.write('q')
           self.process.stdin.flush()
           self.process.wait()
           print("Recording stopped.")
       else:
           print("No recording in progress.")

	
   def stop_screen_grab(self):
       if self.grab_process and self.grab_process.poll() is None:
           self.grab_process.stdin.write('q')
           self.grab_process.stdin.flush()
           self.grab_process.wait()
           print("Screen Grab stopped.")
       else:
           print("No Grab in progress.")
   	
   def start_preview(self):
       if self.streaming_process and self.streaming_process.poll() is None:
           print("Streaming is already in progress.")
           return


       self.streaming_process = subprocess.Popen(
           ['ffmpeg', '-i', 'rtsp://admin:hik@9753@192.168.0.252:554/Streaming/Channels/101',
            '-c:v', 'copy', '-vf', 'scale=390:660','-f', 'hls', f'http://localhost:8000/video_stream'],
           stdin=subprocess.PIPE,
           stdout=subprocess.PIPE,
           stderr=subprocess.PIPE,
           bufsize=1,
           universal_newlines=True
       )
       print(f"Streaming started on port {self.stream_port}.")


   def stop_streaming(self):
       if self.streaming_process and self.streaming_process.poll() is None:
           self.streaming_process.terminate()
           self.streaming_process.wait()
           print("Streaming stopped.")
       else:
           print("No streaming in progress.")


   def get_file_info(self):
       return {"filename": self.filename, "filepath": self.filepath}


   def __del__(self):
       if self.process and self.process.poll() is None:
           self.process.terminate()
           print("FFmpeg recording process terminated on deletion.")
       if self.streaming_process and self.streaming_process.poll() is None:
           self.streaming_process.terminate()
           print("FFmpeg streaming process terminated on deletion.")


