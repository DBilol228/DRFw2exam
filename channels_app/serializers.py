from rest_framework import serializers
from .models import Channel,Following,Post

class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ['id','owner','title','description','type','slug','created_at']
        read_only_fields = ['id','owner','slug','created_at']

class FollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Following
        fields = ['id','user','channel','created_at']
        read_only_fields = ['id','user','channel','created_at']

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id','channel','title','description','content','created_at']
        read_only_fields = ['id','channel','created_at']