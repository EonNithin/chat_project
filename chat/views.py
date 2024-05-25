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

mp3_folderpath = "/home/eon/obs studio/recordings/mp3s"

def ai_process(request):
    return render(request, 'ai_process.html')

def ai_chatpage(request):
    return render(request, 'ai_chatpage.html')

def eonpod(request):
    return render(request, 'eonpod.html')
