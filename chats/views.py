from .models import Chat,Message
from .serializers import ChatSerializer,MessageSerializer
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveDestroyAPIView, ListCreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError, PermissionDenied
from django.shortcuts import get_object_or_404
from django.db.models import Q

class ChatCreateView(CreateAPIView):
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        user_2 = serializer.validated_data['user_2']
        if user_2 == self.request.user:
            raise ValidationError({'user_2':'You cannot create a chat with yourself'})
        if Chat.objects.filter(Q(user_1=self.request.user,user_2=user_2) | Q(user_1=user_2,user_2=self.request.user)).exists():
            raise ValidationError({'detail':'This chat already exists'})
        serializer.save(user_1=self.request.user)

class ChatListView(ListAPIView):
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Chat.objects.filter(Q(user_1=self.request.user) | Q(user_2=self.request.user)).order_by('-created_at')

class ChatDetailView(RetrieveDestroyAPIView):
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Chat.objects.filter(Q(user_1=self.request.user) | Q(user_2 = self.request.user))

class MessageListCreateView(ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    def get_chat(self):
        return get_object_or_404(Chat.objects.filter(Q(user_1=self.request.user) | Q(user_2=self.request.user)),pk=self.kwargs['chat_id'])
    def get_queryset(self):
        chat = self.get_chat()
        return Message.objects.filter(chat=chat).order_by('created_at')
    def perform_create(self, serializer):
        chat = self.get_chat()
        serializer.save(chat=chat,sender=self.request.user)

class MessageDeleteView(DestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    def perform_destroy(self, instance):
        if instance.sender != self.request.user:
            raise PermissionDenied('You can delete only your own messages.')
        instance.delete()