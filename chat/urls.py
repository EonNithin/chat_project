from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from chat.views import eonpod, ai_process, ai_response, ai_chatpage, generate_response, get_latest_mp4_filepath, transcribe_mp3, transcribe_selected_mp3, update_recording_status, update_streaming_status, convert_mp4_to_mp3

urlpatterns = [
    path('', eonpod, name='eonpod'),
    path('ai_process/', ai_process, name='ai_process'),
    path('ai_response/', ai_response, name='ai_response'),
    path('ai_chatpage/', ai_chatpage, name='ai_chatpage'),
    path('transcribe_mp3/', transcribe_mp3, name='transcribe_mp3'),
    path('generate_response/', generate_response, name='generate_response'),
    path('update_recording_status/', update_recording_status, name='update_recording_status'),
    path('update_streaming_status/', update_streaming_status, name='update_streaming_status'),
    path('transcribe_selected_mp3/', transcribe_selected_mp3, name='transcribe_selected_mp3'),
    path('get_latest_mp4_filepath/', get_latest_mp4_filepath, name='get_latest_recording'),
    path('convert_mp4_to_mp3/', convert_mp4_to_mp3, name='convert_mp4_to_mp3'),
    # Add other URL patterns as needed
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
