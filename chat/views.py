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

def get_latest_filepath(directory):
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
    if request.method == 'POST':
        global mp3_folderpath
        latest_file = get_latest_filepath(mp3_folderpath)
        print("\nLatest filepath:\n", latest_file)
        transcribed_text = transcribe_latest_file(latest_file)
        if transcribed_text:
            response_text = llm.invoke(transcribed_text)
            quiz_prompt = f"Generate 3 Multiple Choice Quiz questions with answers for : {response_text}"
            quiz_question = llm.invoke(quiz_prompt)
            response_data = {
                'file_path': latest_file,
                'response_text': response_text,
                'quiz_question': quiz_question
            }
            return JsonResponse(response_data)
        else:
            return JsonResponse({'error': 'Error transcribing uploaded file'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request or missing file'}, status=400)

def whisper_response(request):
    # Implement your logic here if needed
    return render(request, 'whisper_response.html')  # Replace 'different_ui_url_name' with the actual URL name for the different UI

def chat_page(request):
    return render(request, 'chat_page.html')
