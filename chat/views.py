import glob
import json
import os
from django.shortcuts import render, redirect
from django.http import JsonResponse
from langchain_community.llms import Ollama
from whisper_cpp_python import whisper
from django.conf import settings
from chat_project import settings
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from chat.processFiles import process_files
from chat.classes.ProcessingQueue import ProcessingQueue


llm = Ollama(base_url='http://localhost:11434', model="mistral")

# Define the base path for media files
media_folderpath = os.path.join(settings.BASE_DIR, 'media', 'processed_files')

# Initialize the processing queue
processing_queue = ProcessingQueue()

@csrf_exempt
def process_mp4files(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            selected_subject = data.get('subject', '')  # Get the subject from the request
            print(f"Selected subject: {selected_subject}")
            
            # Retrieve the latest MP4 file from the processed_files directory
            mp4_files = [f for f in os.listdir(media_folderpath) if f.endswith('.mp4')]
            if not mp4_files:
                return JsonResponse({"success": False, "error": "No MP4 files found in the processed_files folder"})

            # Assuming you want the most recent file
            latest_mp4_file = max(mp4_files, key=lambda f: os.path.getmtime(os.path.join(media_folderpath, f)))
            mp4_file_path = os.path.join(media_folderpath, latest_mp4_file)
            
            print(f"Latest MP4 file path: {mp4_file_path}")

            # Add the file to the processing queue with both arguments
            processing_queue.add_to_queue(latest_mp4_file, mp4_file_path, selected_subject)

            return JsonResponse({
                "success": True,
                "message": "File added to processing queue",
                "mp4_filepath": mp4_file_path,
                "filename": latest_mp4_file
            })
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    return JsonResponse({"success": False, "error": "Invalid request method"})


def get_latest_mp4_filepath(request):
    try:
        # List all folders in the media directory
        folders = [f for f in os.listdir(media_folderpath) if os.path.isdir(os.path.join(media_folderpath, f))]
        
        if not folders:
            return JsonResponse({'error': 'No folders found'}, status=404)

        # Get the latest folder based on modification time
        latest_folder = max(folders, key=lambda f: os.path.getmtime(os.path.join(media_folderpath, f)))
        latest_folder_path = os.path.join(media_folderpath, latest_folder)
        
        # List all MP4 files inside the latest folder
        mp4_files = [f for f in os.listdir(latest_folder_path) if f.endswith('.mp4')]

        if not mp4_files:
            return JsonResponse({'error': 'No MP4 files found in the latest folder'}, status=404)

        # Assuming there's only one MP4 file in the latest folder, get its path
        latest_mp4 = os.path.join(latest_folder_path, mp4_files[0])

        # Construct the media URL for the latest MP4 file
        media_url = os.path.join(settings.MEDIA_URL, 'processed_files', latest_folder, mp4_files[0]).replace("\\", "/")
        print("\nMedia URL is:\n", media_url)
        
        return JsonResponse({'latest_file': media_url})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

conversation_history = []

def ollama_generate_response(question):
    try:
        global conversation_history
        # full_prompt = "\n".join(conversation_history)
        response_text = llm.invoke(question)
        # print("success invoking ollama mistral model")
        #conversation_history.append(response_text)
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