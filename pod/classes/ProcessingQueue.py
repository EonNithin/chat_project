import threading
import time
import os
from pod.processFiles import process_files

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
                files_to_delete = []
                for file_name, data in list(self.mp4_paths.items()):
                    if data["status"] == "NotStarted":
                        print(f"Processing file: {file_name}")
                        self.mp4_paths[file_name]["status"] = "InProgress"
                        subject = data["subject"]
                        file_path = data["file_path"]  # Retrieve the correct file path
                        self.lock.release()  # Release the lock before processing
                        try:
                            # Process the file with the subject
                            process_files(file_name, file_path, subject)
                            with self.lock:
                                files_to_delete.append(file_name)
                        except Exception as e:
                            print(f"Error processing file {file_name}: {str(e)}")
                            with self.lock:
                                self.mp4_paths[file_name]["status"] = f"Error: {str(e)}"
                        finally:
                            self.lock.acquire()  # Reacquire the lock

                for file_name in files_to_delete:
                    del self.mp4_paths[file_name]
                    print(f"File processed and removed from queue: {file_name}")

            # Debug print to monitor thread execution
            print("Sleeping for 1000 seconds...")
            time.sleep(1000)