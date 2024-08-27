from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from pod.views import eonpod, ai_chatpage, process_mp4files, generate_response, get_latest_mp4_filepath, update_recording_status, update_streaming_status

urlpatterns = [
    path('', eonpod, name='eonpod'),
    path('ai_chatpage/', ai_chatpage, name='ai_chatpage'),
    path('process_mp4files/', process_mp4files, name='process_mp4files'),
    path('generate_response/', generate_response, name='generate_response'),
    path('update_recording_status/', update_recording_status, name='update_recording_status'),
    path('update_streaming_status/', update_streaming_status, name='update_streaming_status'),
    path('get_latest_mp4_filepath/', get_latest_mp4_filepath, name='get_latest_recording'),
    # Add other URL patterns as needed
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
