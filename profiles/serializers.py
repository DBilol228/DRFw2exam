from rest_framework import serializers
from .models import Profile,Avatar

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id','user','username','first_name','last_name','bio']
        read_only_fields = ['id','user']

class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avatar
        fields = ['id','profile','image','created_at']
        read_only_fields = ['id','profile','created_at']