import threading
import time
import os
from django.conf import settings
from pod.processFiles import process_files

# Define the base path for media files
media_folderpath = os.path.join(settings.BASE_DIR, 'media', 'processed_files')

class ProcessingQueue:
    def __init__(self):
        self.mp4_paths = {}
        self.lock = threading.Lock()
        self.processing_thread = threading.Thread(target=self.process_queue)
        self.processing_thread.daemon = True
        self.processing_thread.start()

    def add_to_queue(self, file_name, file_path, subject):
        with self.lock:
            self.mp4_paths[file_name] = {"file_path": file_path, "status": "NotStarted", "subject": subject}
        print(f"Added to queue: {file_name} with path: {file_path}")


    def process_queue(self):
        while True:
            with self.lock:
                # Find the latest folder in processed_files
                folders = [f for f in os.listdir(media_folderpath) if os.path.isdir(os.path.join(media_folderpath, f))]
                if not folders:
                    print("No folders found in processed_files.")
                    time.sleep(100)
                    continue
                
                latest_folder = max(folders, key=lambda f: os.path.getmtime(os.path.join(media_folderpath, f)))
                folder_path = os.path.join(media_folderpath, latest_folder)
                
                # Find the latest MP4 file in the latest folder
                mp4_files = [f for f in os.listdir(folder_path) if f.endswith('.mp4')]
                if not mp4_files:
                    print(f"No MP4 files found in the latest folder: {folder_path}")
                    time.sleep(100)
                    continue
                
                latest_mp4_file = max(mp4_files, key=lambda f: os.path.getmtime(os.path.join(folder_path, f)))
                mp4_file_path = os.path.join(folder_path, latest_mp4_file)
                
                print(f"Processing file: {latest_mp4_file}")
                
                # Add the file to the processing queue with the folder path
                # Call process_file function in process_files.py file
                self.process_file(latest_mp4_file, mp4_file_path, folder_path)
                
            # Debug print to monitor thread execution
            print("Sleeping for 100 seconds...")
            time.sleep(100)

