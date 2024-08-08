import glob
import json
import os
import subprocess
from django.shortcuts import render, redirect
from django.http import JsonResponse
from langchain_community.llms import Ollama
from whisper_cpp_python import whisper
from django.conf import settings
from chat_project import settings
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from moviepy.editor import VideoFileClip
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from summarizer.bert import Summarizer, TransformerSummarizer
from fpdf import FPDF
from PyPDF2 import PdfReader


# Initialize Ollama outside the view
llm = Ollama(
    base_url='http://localhost:11434',
    model="mistral"
)

# Initializing bert-summarizer model
bert_model = Summarizer()

# Initialize the model
whisper_model = whisper.Whisper(model_path="/home/eon/Desktop/Whisper/whisper.cpp/models/ggml-base.en.bin")

conversation_history = []

files_location = "/home/eon/VSCodeProjects/eonpod-project"
mp3_folderpath = os.path.join(settings.BASE_DIR, "media", "mp3s")
mp4_folderpath = os.path.join(settings.BASE_DIR, "media", "mp4s")

print("mp4 folder path is :\n", mp4_folderpath)

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
        print("\nmedia url is :\n", media_url)
        return JsonResponse({'latest_file': media_url})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def summarize_transcription(transcribed_text):
    bert_summary = ''.join(bert_model(body = transcribed_text, min_length = 60))
    return bert_summary

def ollama_generate_response(question):
    try:
        global conversation_history
        conversation_history.append(question)
        full_prompt = "\n".join(conversation_history)
        response_text = llm.invoke(full_prompt)
        print("success invoking ollama mistral model")
        conversation_history.append(response_text)
        print("Response:\n", response_text, "\n")
        return response_text
    except Exception as e:
        return "error generating response: {e}"

@csrf_exempt
def generate_response(request):
    if request.method == 'POST':
        try:
            question = request.POST.get('question', '')
            if not question:
                print("POST data is empty or question is not in POST data.")
                print("Request body:\n", request.body.decode('utf-8'))
                print("Request POST:\n", request.POST)
            print("Question is : \n", question)
            response = ollama_generate_response(question)
            print("Response is : \n", response)
            return JsonResponse({'question': question, 'response': response})
        except Exception as e:
            print(f"Error processing request: {e}")
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def ai_process(request):
    return render(request, 'ai_process.html')

def ai_chatpage(request):
    return render(request, 'ai_chatpage.html')

recording_status = False

@csrf_exempt
def update_recording_status(request):
    global recording_status
    if request.method == 'POST':
        data = json.loads(request.body)
        print("data:", data)
        recording_status = data.get('is_recording')
        print("recording status inside:",recording_status)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'}, status=400)

streaming_status = False

@csrf_exempt
def update_streaming_status(request):
    global streaming_status
    if request.method == 'POST':
        data = json.loads(request.body)
        print("data:", data)
        streaming_status = data.get('is_streaming', False)
        print("streaming status inside:",streaming_status)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'}, status=400)

def eonpod(request):
    global recording_status, streaming_status
    return render(request, 'eonpod.html', {
        'is_recording': recording_status,
        'is_streaming': streaming_status
    })