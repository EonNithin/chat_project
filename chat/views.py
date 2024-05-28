import os
from django.shortcuts import render, redirect
from django.http import JsonResponse
from langchain_community.llms import Ollama
import whisper
from django.conf import settings
from chat_project import settings
from django.http import JsonResponse, HttpResponseBadRequest

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
        print("\nmedia url is :\n", media_url)
        return JsonResponse({'latest_file': media_url})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_latest_mp3_filepath(directory):
    # Get a list of all files in the directory
    files = [os.path.join(directory, file) for file in os.listdir(directory)]
    
    # Filter out directories (if any)
    files = [file for file in files if os.path.isfile(file)]
    
    # Sort files based on modification time (descending order)
    files.sort(key=os.path.getmtime, reverse=True)
    
    # Return the path of the most recent file
    if files:
        return files[0]
    else:
        return None

def transcribe_latest_file(latest_file):
    try:
        # Transcribe the uploaded file using Whisper
        model = whisper.load_model("base")
        result = model.transcribe(latest_file)
        print("\nresponse from whisper:\n", result["text"])
        # Return the transcribed text
        return result["text"]
    except Exception as e:
        print("Error transcribing uploaded file:", e)
        return None

def transcribe_mp3(request):
    if request.method == 'GET':
        global mp3_folderpath
        latest_file = get_latest_mp3_filepath(mp3_folderpath)
        print("\nLatest filepath:\n", latest_file)
        transcribed_text = transcribe_latest_file(latest_file)
        if transcribed_text:
            response_text = llm.invoke(transcribed_text)
            quiz_prompt = f"Generate 3 Multiple Choice Quiz questions with answers for : {response_text}"
            quiz_question = llm.invoke(quiz_prompt)
            print("Quiz Questions are:\n", quiz_question)
            response_data = {
                'file_path': latest_file,
                'response_text': response_text,
                'quiz_question': quiz_question
            }
            return JsonResponse(response_data)
        else:
            return JsonResponse({'error': 'Error transcribing uploaded file'}, status=500)
    else:
        return HttpResponseBadRequest('Invalid request method')


def ai_process(request):
    return render(request, 'ai_process.html')

def ai_response(request):
    return render(request, 'ai_response.html')

def ai_chatpage(request):
    return render(request, 'ai_chatpage.html')

def eonpod(request):
    return render(request, 'eonpod.html')
