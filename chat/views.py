import os
from django.shortcuts import render, redirect
from django.http import JsonResponse
from langchain_community.llms import Ollama
import whisper

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
    if request.method == 'POST' and request.FILES['file']:
        # Save the uploaded file to a local folder
        uploaded_file = request.FILES['file']
        print("Uploaded file path is :", uploaded_file)
        file_path = os.path.join(settings.MEDIA_ROOT, 'mp3s', uploaded_file.name)
        with open(file_path, 'wb') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        # Transcribe the saved file using Whisper
        result = whisper.load_model("base").transcribe(file_path)

        # Invoke Ollama with the transcribed text
        response_text = llm.invoke(result["text"])

        return JsonResponse({'response_text': response_text})

    return JsonResponse({'error': 'Invalid request'}, status=400)

def whisper_response(request):
    # Implement your logic here if needed
    return render(request, 'whisper_response.html')  # Replace 'different_ui_url_name' with the actual URL name for the different UI

def chat_page(request):
    return render(request, 'chat_page.html')
