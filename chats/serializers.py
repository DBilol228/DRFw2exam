from rest_framework import serializers
from .models import Chat,Message

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['id','user_1','user_2','created_at']
        read_only_fields = ['id','created_at']

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id','chat','sender','content','created_at']
        read_only_fields = ['id','sender','created_at']