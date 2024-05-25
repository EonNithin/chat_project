from django.urls import path, include
from chat.views import eonpod, ai_process, ai_chatpage

urlpatterns = [
    path('', eonpod, name='eonpod'),
    path('ai_process/', ai_process, name='ai_process'),
    path('ai_chatpage/', ai_chatpage, name='ai_chatpage'),
    # Add other URL patterns as needed
]
