import glob
import os
import json
from django.conf import settings
from moviepy.editor import VideoFileClip
from whisper_cpp_python import whisper
from summarizer.bert import Summarizer
from langchain_community.llms import Ollama
from django.http import JsonResponse
import socket

# Initialize the models
whisper_model = whisper.Whisper(model_path=os.path.join(settings.BASE_DIR, 'models', 'ggml-base.en.bin'))
bert_model = Summarizer()
llm = Ollama(base_url='http://localhost:11434', model="mistral")

# Define the base path for media files
media_folderpath = os.path.join(settings.BASE_DIR, 'media', 'processed_files')

def get_device_name():
    try:
        return socket.gethostname()
    except Exception as e:
        print(f"Error getting device name: {e}")
        return "unknown_device"

def summarize_transcription(transcribed_text):
    return ''.join(bert_model(body=transcribed_text, min_length=30))

def transcribe_mp3file(mp3_filepath):
    try:
        result = whisper_model.transcribe(mp3_filepath)
        print("\nResponse from Whisper:\n", result["text"])
        return result["text"]
    except Exception as e:
        print(f"\nError transcribing MP3: {e}\n")
        return None

def generate_quiz(summary_text):
    try:
        quiz_prompt = f"\nGenerate 3 Multiple Choice Quiz questions with answers for: {summary_text}\n"
        quiz_questions = llm.invoke(quiz_prompt)
        print("Quiz Questions are:\n", quiz_questions)
        return quiz_questions.strip().split('\n\n')  # Assuming each question is separated by two newlines
    except Exception as e:
        return [f"\nError generating questions: {e}\n"]

def save_text_as_file(text, file_path):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(text)
        print(f"\nText file saved to: {file_path}\n")
    except Exception as e:
        print(f"\nError saving text file {file_path}: {e}\n")

def load_text_from_file(txt_filepath):
    try:
        with open(txt_filepath, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"\nError loading text from file {txt_filepath}: {e}\n")
        return ""



def process_files(mp4_filename, mp4_filepath, subject, codec="libmp3lame"):
    try:
        # Get device name
        device_name = get_device_name()

        # Define the folder path based on the provided filename and subject
        custom_foldername = f"{device_name}_{os.path.splitext(mp4_filename)[0]}_{subject}"
        folder_path = os.path.join(media_folderpath, custom_foldername)

        # Define the file paths for the expected outputs
        processed_mp4_filepath = os.path.join(folder_path, mp4_filename)
        mp3_filepath = os.path.join(folder_path, f"{os.path.splitext(mp4_filename)[0]}.mp3")
        transcription_txt_filepath = os.path.join(folder_path, f"{os.path.splitext(mp4_filename)[0]}_transcription.txt")
        summary_txt_filepath = os.path.join(folder_path, f"{os.path.splitext(mp4_filename)[0]}_summary.txt")
        quiz_txt_filepath = os.path.join(folder_path, f"{os.path.splitext(mp4_filename)[0]}_quiz.txt")

        # Create the folder if it doesn't exist
        os.makedirs(folder_path, exist_ok=True)

        # Move the original MP4 file to the destination folder if not already moved
        if not os.path.exists(processed_mp4_filepath):
            print(f"\nMoving original MP4 file {mp4_filepath} to {processed_mp4_filepath}...\n")
            os.rename(mp4_filepath, processed_mp4_filepath)

        # Process the MP3 file if MP3 is missing
        if not os.path.exists(mp3_filepath):
            print(f"\nExtracting audio from {processed_mp4_filepath}...\n")
            video_clip = VideoFileClip(processed_mp4_filepath)
            audio_clip = video_clip.audio
            audio_clip.write_audiofile(mp3_filepath, codec=codec)
            print(f"\nSuccessfully converted {processed_mp4_filepath} to {mp3_filepath}\n")

        # Process the transcription if transcription TXT is missing
        transcribed_text = None
        if not os.path.exists(transcription_txt_filepath):
            if os.path.exists(mp3_filepath):
                print("Starting transcription process...")
                transcribed_text = transcribe_mp3file(mp3_filepath)
                if transcribed_text:
                    save_text_as_file(transcribed_text, transcription_txt_filepath)
                    print(f"\nTranscription TXT saved to: {transcription_txt_filepath}\n")

        # Process the summary if summary TXT is missing
        summary_text = None
        if not os.path.exists(summary_txt_filepath):
            if os.path.exists(transcription_txt_filepath):
                print("Starting summarization process...")
                if transcribed_text is None:
                    transcribed_text = load_text_from_file(transcription_txt_filepath)
                summary_text = summarize_transcription(transcribed_text)
                if summary_text:
                    save_text_as_file(summary_text, summary_txt_filepath)
                    print(f"\nSummary TXT saved to: {summary_txt_filepath}\n")

        # Process the quiz if quiz TXT is missing
        if not os.path.exists(quiz_txt_filepath):
            if os.path.exists(summary_txt_filepath):
                print("Starting quiz generation process...")
                if summary_text is None:
                    summary_text = load_text_from_file(summary_txt_filepath)
                quiz = generate_quiz(summary_text)
                save_text_as_file('\n\n'.join(quiz), quiz_txt_filepath)
                print(f"\nQuiz TXT saved to: {quiz_txt_filepath}\n")

        print(f"\nProcessing complete for {mp4_filename}\n")

        return JsonResponse({"success": True})

    except Exception as e:
        print(f"Error: {e}")
        return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Invalid request method"})