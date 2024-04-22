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

def transcribe_uploaded_file(uploaded_file):
    # Define the directory where you want to save the uploaded file temporarily
    temp_dir = os.path.join(settings.MEDIA_ROOT, 'mp3s')

    # Create the temporary directory if it doesn't exist
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    # Save the uploaded file to the temporary directory
    file_path = os.path.join(temp_dir, uploaded_file.name)
    with open(file_path, 'wb') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)

    # Transcribe the saved file using Whisper
    model = whisper.load_model("base")
    result = model.transcribe(file_path)
    print("response from whisper:", result["text"])

    # Return the transcribed text
    return result["text"]

def transcribe_mp3(request):
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']
        transcribed_text = transcribe_uploaded_file(uploaded_file)
        print("\nTranscribed Text:\n", transcribed_text,"\n")
        response_text = llm.invoke(transcribed_text)
        print("\nResponse Text:\n", response_text)
         # Create a JSON response with both transcribed text and response text
        response_data = {
            'transcribed_text': transcribed_text,
            'response_text': response_text
        }
        
        # Return the JSON response
        return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)


def whisper_response(request):
    # Implement your logic here if needed
    return render(request, 'whisper_response.html')  # Replace 'different_ui_url_name' with the actual URL name for the different UI

def chat_page(request):
    return render(request, 'chat_page.html')
