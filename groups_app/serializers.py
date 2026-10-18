from rest_framework import serializers
from .models import Group,GroupMember,GroupMessage

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id','title','owner','avatar','created_at']
        read_only_fields = ['id','owner','created_at']

class GroupMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMember
        fields = ['id','group','user','role','joined_at']
        read_only_fields = ['id','group','joined_at']

class GroupMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMessage
        fields = ['id','group','author','content','created_at']
        read_only_fields = ['id','author','created_at']