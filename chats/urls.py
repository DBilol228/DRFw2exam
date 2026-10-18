from django.urls import path
from .views import ChatCreateView,ChatListView,ChatDetailView,MessageListCreateView,MessageDeleteView

urlpatterns = [
    path('', ChatListView.as_view(), name='chat-list'),
    path('create/', ChatCreateView.as_view(), name='chat-create'),
    path('<int:pk>/', ChatDetailView.as_view(), name='chat-detail'),
    path('<int:chat_id>/messages/', MessageListCreateView.as_view(), name='message-list-create'),
    path('messages/<int:pk>/delete/', MessageDeleteView.as_view(), name='message-delete'),
]