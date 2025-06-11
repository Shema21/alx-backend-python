from django.urls import path

from .views import delete_user, get_conversation_api, unread_messages

urlpatterns = [
    path('delete-account/', delete_user, name='delete_user'),
    path('get-conversation/', get_conversation_api, name='get_conversation_api'),
    path('messages/unread/', unread_messages, name='unread_messages'),
]
