from .models import Profile, Avatar
from .serializers import ProfileSerializer, AvatarSerializer
from rest_framework.generics import RetrieveAPIView, UpdateAPIView, ListAPIView, CreateAPIView, RetrieveDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from rest_framework.exceptions import PermissionDenied
from rest_framework import serializers
from rest_framework.parsers import MultiPartParser, FormParser

class ProfileDetailView(RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

class MyProfileView(UpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['patch','options','head']
    def get_object(self):
        profile, created = Profile.objects.get_or_create(user=self.request.user,defaults={'username': self.request.user.username or self.request.user.phone_number})
        return profile

class ProfileListView(ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['first_name','last_name','username']

class AvatarCreateView(CreateAPIView):
    serializer_class = AvatarSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    def perform_create(self, serializer):
        profile, created = Profile.objects.get_or_create(user=self.request.user,defaults={'username': self.request.user.username or self.request.user.phone_number})
        image = self.request.FILES.get('image')
        if not image:
            raise serializers.ValidationError({'image': 'Image is required.'})
        if image.size > 5 * 1024 * 1024:
            raise serializers.ValidationError({'image': 'Image must not exceed 5 MB.'})
        if image.content_type not in ['image/jpeg','image/png','image/webp']:
            raise serializers.ValidationError({'image': 'Only JPEG, PNG and WEBP images are allowed.'})
        serializer.save(profile=profile)

class AvatarDetailView(RetrieveDestroyAPIView):
    queryset = Avatar.objects.all()
    serializer_class = AvatarSerializer
    permission_classes = [IsAuthenticated]
    def perform_destroy(self, instance):
        if instance.profile.user != self.request.user:
            raise PermissionDenied('You can delete only your own avatar.')
        instance.delete()