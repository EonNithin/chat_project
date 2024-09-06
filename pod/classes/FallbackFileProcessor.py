import os
import FileProcessor


class FallbackFileProcessor:
    def __init__(self):
        # Initialize the FileProcessor instance
        self.processor = FileProcessor()

    
    def process_folders(self):
        # Get all folders in the media_folderpath
        folders = [f for f in os.listdir(self.processor.media_folderpath) if os.path.isdir(os.path.join(self.processor.media_folderpath, f))]

        # Iterate through each folder
        for folder in folders:
            folder_path = os.path.join(self.processor.media_folderpath, folder)
            files = os.listdir(folder_path)
            
            # Check if there are 6 files in the folder
            if len(files) == 6:
                continue  # Skip processing if file count is 6
            
            # Sort files by modification time, latest first
            files_with_paths = [os.path.join(folder_path, f) for f in files]
            latest_file = max(files_with_paths, key=os.path.getmtime)

             # Process the latest file based on its extension
            if latest_file.endswith('.mp3') and not any(f.endswith('_transcript.txt') for f in files):
                transcript = self.processor.mp3_to_transcript(latest_file)
                if transcript:
                    print(f"Transcript processed for {os.path.basename(latest_file)}")

            elif latest_file.endswith('_transcript.txt') and not any(f.endswith('_summary.txt') for f in files):
                summary = self.processor.transcript_to_summary(latest_file)
                if summary:
                    print(f"Summary processed for {os.path.basename(latest_file)}")

            elif latest_file.endswith('_summary.txt') and not any(f.endswith('_quiz.txt') for f in files):
                quiz = self.processor.summary_to_quiz(latest_file)
                if quiz:
                    print(f"Quiz processed for {os.path.basename(latest_file)}")


