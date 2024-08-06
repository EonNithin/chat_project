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

files_location = "/home/eon/VSCodeProjects/eonpod-project"


def compress_mp4(input_file, output_file, codec='libx264', crf=23):
    """
    Compress an MP4 file to a smaller size using ffmpeg.
    """
    try:
        command = [
            'ffmpeg',
            '-i', input_file,       # Input file
            '-vcodec', codec,       # Video codec
            '-crf', str(crf),       # Compression quality
            '-preset', 'slow',      # Compression speed/quality tradeoff
            output_file             # Output file
        ]

        # Run the command
        subprocess.run(command, check=True)
        print(f"Compressed video saved to: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error compressing MP4: {e}")

def convert_mp4_to_mp3(request, codec="libmp3lame"):
    files = glob.glob(os.path.join(mp4_folderpath, '*.mp4'))
    files.sort(key=os.path.getmtime, reverse=True)
    input_mp4 = files[0] if files else None

    if not input_mp4:
        print("No MP4 file to convert.")
        return "Error No file found"
    
    try:
        # Get filename without extension from input path
        filename, _ = os.path.splitext(os.path.basename(input_mp4))

        # Create a new folder with the name of the MP4 file inside the files_location
        folder_path = os.path.join(files_location, filename)
        os.makedirs(folder_path, exist_ok=True)

        # Construct compressed MP4 filename and path inside the created folder
        compressed_mp4_filepath = os.path.join(folder_path, filename + "_compressed.mp4")
        # Compress the MP4 file
        compress_mp4(input_mp4, compressed_mp4_filepath)
        
        # Construct output MP3 filename with .mp3 extension inside the created folder
        mp3_filepath = os.path.join(folder_path, filename + ".mp3")

        # Load the compressed MP4 file
        video_clip = VideoFileClip(compressed_mp4_filepath)
        print("Extracting audio from compressed MP4...")

        # Extract audio from the video
        audio_clip = video_clip.audio
        
        # Write the audio to an MP3 file with specified codec
        audio_clip.write_audiofile(mp3_filepath, codec=codec)
        print(f"Successfully converted {compressed_mp4_filepath} to {mp3_filepath}")

        return JsonResponse({"success": True, "mp3_filepath": mp3_filepath})
    except Exception as e:
        print(f"Error converting MP4: {e}")
        return JsonResponse({"success": False, "error": str(e)})


def transcribe_latest_file(latest_file):
    try:
        result = whisper_model.transcribe(latest_file)
        print("\nresponse from whisper:\n", result["text"])
        # Return the transcribed text
        return result["text"]
    except Exception as e:
        print("Error transcribing uploaded file:", e)
        return None

def summarize_transcription(transcribed_text):
    bert_summary = ''.join(bert_model(body = transcribed_text, min_length = 60))
    return bert_summary

def transcribe_mp3(request):
    if request.method == 'GET':
        global mp3_folderpath
        latest_file = get_latest_mp3_filepath(mp3_folderpath)
        print("\nLatest filepath:\n", latest_file)
        transcribed_text = transcribe_latest_file(latest_file)
        if transcribed_text:
            print("transcribed text is :\n", transcribed_text)
            bert_summary = summarize_transcription(transcribed_text)
            print("Response summary is \n", bert_summary)
            response_data = {
                'file_path': latest_file,
                'transcribed_text': transcribed_text,
                'response_text': bert_summary,
            }
            return JsonResponse(response_data)
        else:
            return JsonResponse({'error': 'Error transcribing uploaded file'}, status=500)
    else:
        return HttpResponseBadRequest('Invalid request method')

@csrf_exempt
def transcribe_selected_mp3(request):
    if request.method == 'POST':
        # Check if a file is uploaded
        if 'file' not in request.FILES:
            return JsonResponse({'error': 'No file uploaded'}, status=400)

        uploaded_file = request.FILES['file']
        file_path = os.path.join(mp3_folderpath, uploaded_file.name)
        print("\nfile uploaded is :\n", file_path)
        # Save the uploaded file
        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
                
        # Transcribe the uploaded file using Whisper
        try:
            result =  whisper_model.transcribe(file_path)
            transcribed_text = result["text"]
            print("\nresult of transcribed selected file:\n", transcribed_text)

            # Generate a response from bert-summerizer
            bert_summary = summarize_transcription(transcribed_text)
            print("Response summary is \n", bert_summary)
            response_data = {
                'transcribed_text': transcribed_text,
                'response_text': bert_summary,
            }
            return JsonResponse(response_data)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return HttpResponseBadRequest('Invalid request method')

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