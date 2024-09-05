import os
import json
from django.conf import settings
from moviepy.editor import VideoFileClip
from whisper_cpp_python import whisper
from summarizer.bert import Summarizer
from langchain_community.llms import Ollama
from django.http import JsonResponse


class FileProcessor:
    def __init__(self):
        # Initialize the models
        self.whisper_model = whisper.Whisper(model_path=os.path.join(settings.BASE_DIR, 'models', 'ggml-base.en.bin'))
        self.bert_model = Summarizer()
        self.llm = Ollama(base_url='http://localhost:11434', model="mistral")
        # Define the base path for media files
        self.media_folderpath = os.path.join(settings.BASE_DIR, 'media', 'processed_files')


    def mp4_to_mp3(self, mp4_filepath):
        # Convert MP4 to MP3 using moviepy or another method
        mp3_filepath = mp4_filepath.replace('.mp4', '.mp3') 
        try:
            video = VideoFileClip(mp4_filepath)
            audio = video.audio
            audio.write_audiofile(mp3_filepath)
            print(f"\nMP3 file saved to: {mp3_filepath}\n")
            return self.mp3_to_transcript(mp3_filepath)
        except Exception as e:
            print(f"\nError converting MP4 to MP3: {e}\n")
            return None

    def mp3_to_transcript(self, mp3_filepath):
        try:
            result = self.whisper_model.transcribe(mp3_filepath)
            transcript_text = result["text"]
            print("\nResponse from Whisper:\n", transcript_text)
            # Define the path to save the transcript file
            transcript_filepath = mp3_filepath.replace('.mp3', '_transcript.txt')
            # Save the transcript to a text file
            self.save_text_as_file(transcript_text, transcript_filepath)
            return self.transcript_to_summary(transcript_text)
        except Exception as e:
            print(f"\nError transcribing MP3: {e}\n")
            return None

    def transcript_to_summary(self, transcript_filepath):
        try:
            transcript = self.load_text_from_file(transcript_filepath)
            summary = ''.join(self.bert_model(body=transcript, min_length=30))
            print("\nSummary generated:\n", summary)
            # Define the path to save the summary file
            summary_filepath = transcript_filepath.replace('_transcript.txt', '_summary.txt')
            # Save the summary to a text file
            self.save_text_as_file(summary, summary_filepath)
            return self.summary_to_quiz(summary_filepath)
        except Exception as e:
            print(f"\nError generating summary: {e}\n")
            return None

    def summary_to_quiz(self, summary_filepath):
        try:
            summary = self.load_text_from_file(summary_filepath)
            quiz_prompt = f"\nGenerate 3 Multiple Choice Quiz questions with answers for: {summary}\n"
            quiz_questions = self.llm.invoke(quiz_prompt)
            print("Quiz Questions are:\n", quiz_questions)
            # Define the path to save the quiz file
            quiz_filepath = summary_filepath.replace('_summary.txt', '_quiz.txt')
            # Save the quiz to a text file
            self.save_text_as_file(quiz_questions, quiz_filepath)
            return quiz_questions.strip().split('\n\n')  # Assuming each question is separated by two newlines
        except Exception as e:
            print(f"\nError generating quiz questions: {e}\n")
            return [f"\nError generating questions: {e}\n"]


    def save_text_as_file(self, text, file_path):
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(text)
            print(f"\nText file saved to: {file_path}\n")
        except Exception as e:
            print(f"\nError saving text file {file_path}: {e}\n")

    def load_text_from_file(self, txt_filepath):
        try:
            with open(txt_filepath, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            print(f"\nError loading text from file {txt_filepath}: {e}\n")
            return ""