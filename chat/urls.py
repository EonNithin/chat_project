from django.urls import path, include
from chat.views import chat_page, generate_response, whisper_response

urlpatterns = [
    path('', chat_page, name='chat_page'),
    path('generate_response/', generate_response, name='generate_response'),
    path('whisper_response/', whisper_response, name='whisper_response'),
    # Add other URL patterns as needed
]
