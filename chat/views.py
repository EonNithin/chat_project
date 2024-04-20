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

def ollama_generate_response(question):
    global conversation_history
    conversation_history.append(question)
    full_prompt = "\n".join(conversation_history)
    response_text = llm.invoke(full_prompt)
    conversation_history.append(response_text)
    print("Response:\n", response_text, "\n")
    return response_text

def generate_response(request):
    if request.method == 'POST':
        question = request.POST.get('question', '')
        print("Question is : \n", question)
        response = ollama_generate_response(question)
        print("Response is : \n", response)
        return JsonResponse({'question': question, 'response': response})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def transcribe_mp3(request):
    if request.method == 'POST' and request.FILES.get('file'):
        # Save the uploaded file to the mp3s directory within MEDIA_ROOT
        uploaded_file = request.FILES['file']
        print("uploaded file:\n", uploaded_file, "\n")
        

    
        # Implement the rest of your logic (transcription, etc.) here

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'error': 'No file uploaded'}, status=400)


def whisper_response(request):
    # Implement your logic here if needed
    return render(request, 'whisper_response.html')  # Replace 'different_ui_url_name' with the actual URL name for the different UI

def chat_page(request):
    return render(request, 'chat_page.html')
