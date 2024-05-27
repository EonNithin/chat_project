import os
from django.shortcuts import render, redirect
from django.http import JsonResponse
from langchain_community.llms import Ollama
import whisper
from django.conf import settings
from chat_project import settings

# Initialize Ollama outside the view
llm = Ollama(model="mistral")
conversation_history = []

mp3_folderpath = os.path.join(settings.BASE_DIR, "media", "mp3s")
mp4_folderpath = os.path.join(settings.BASE_DIR, "media", "mp4s")

def get_latest_mp4_filepath(request):
    try:
        # List all files in the directory
        files = [f for f in os.listdir(mp4_folderpath) if os.path.isfile(os.path.join(mp4_folderpath, f))]
        
        if not files:
            return JsonResponse({'error': 'No files found'}, status=404)

        # Get the latest file based on modification time
        latest_file = max(files, key=lambda f: os.path.getmtime(os.path.join(mp4_folderpath, f)))

        # Construct the media URL for the latest file
        media_url = os.path.join(settings.MEDIA_URL, 'mp4s', latest_file).replace("\\", "/")

        return JsonResponse({'latest_file': media_url})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def ai_process(request):
    return render(request, 'ai_process.html')

def ai_chatpage(request):
    return render(request, 'ai_chatpage.html')

def eonpod(request):
    return render(request, 'eonpod.html')
