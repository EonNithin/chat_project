from django.urls import path, include
from chat.views import chat_page, generate_response, whisper_response, transcribe_mp3, obs_recording

urlpatterns = [
    path('', chat_page, name='chat_page'),
    path('generate_response/', generate_response, name='generate_response'),
    path('transcribe_mp3/', transcribe_mp3, name='transcribe_mp3'),
    path('whisper_response/', whisper_response, name='whisper_response'),
    path('obs_recording/', obs_recording, name='obs_recording'),
    # Add other URL patterns as needed
]
