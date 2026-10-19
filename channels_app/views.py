from .models import Channel,Following,Post
from .serializers import ChannelSerializer,FollowingSerializer,PostSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied, ValidationError
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import HTTP_201_CREATED,HTTP_204_NO_CONTENT

class ChannelListCreateView(ListCreateAPIView):
    serializer_class = ChannelSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Channel.objects.filter(Q(type='public') | Q(owner=self.request.user)).distinct().order_by('-created_at')
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ChannelDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = ChannelSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get','patch','delete','options','head']
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Channel.objects.filter(type='public')
        return Channel.objects.filter(
            Q(type='public') |
            Q(owner=self.request.user) |
            Q(followers__user=self.request.user)
        ).distinct()
    def perform_update(self, serializer):
        if serializer.instance.owner != self.request.user:
            raise PermissionDenied('Only the channel owner can edit this channel')
        serializer.save()
    def perform_destroy(self, instance):
        if instance.owner != self.request.user:
            raise PermissionDenied('Only the channel owner can delete this channel')
        instance.delete()

class FollowChannelView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, channel_id):
        channel = get_object_or_404(Channel,pk=channel_id)
        if channel.type == 'private' and channel.owner != request.user:
            raise PermissionDenied('You cannot follow this private channel.')
        if Following.objects.filter(user=request.user,channel=channel).exists():
            raise ValidationError({'detail':'You already follow this channel.'})
        following = Following.objects.create(user=request.user,channel=channel)
        return Response(FollowingSerializer(following).data,status=HTTP_201_CREATED)

    def delete(self, request, channel_id):
        following = get_object_or_404(Following,user=request.user,channel_id=channel_id)
        following.delete()
        return Response(status=HTTP_204_NO_CONTENT)

class FollowingListView(ListAPIView):
    serializer_class = FollowingSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Following.objects.filter(user=self.request.user).order_by('-created_at')

class IsFollowingView(RetrieveAPIView):
    serializer_class = FollowingSerializer
    permission_classes = [IsAuthenticated]
    def retrieve(self, request, *args, **kwargs):
        channel = get_object_or_404(Channel,pk=self.kwargs['channel_id'])
        is_following = Following.objects.filter(user=request.user,channel=channel).exists()
        return Response({'channel_id':channel.id,'is_following':is_following})

class PostListCreateView(ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    def get_channel(self):
        return get_object_or_404(Channel,pk=self.kwargs['channel_id'])
    def check_access(self,channel):
        if channel.type == 'private' and channel.owner != self.request.user and not Following.objects.filter(user=self.request.user,channel=channel).exists():
            raise PermissionDenied('You do not have access to this private channel')
    def get_queryset(self):
        channel = self.get_channel()
        self.check_access(channel)
        return Post.objects.filter(channel=channel).order_by('-created_at')
    def perform_create(self, serializer):
        channel = self.get_channel()
        if channel.owner != self.request.user:
            raise PermissionDenied('Only the channel owner can create posts')
        serializer.save(channel=channel)

class PostDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get','patch','delete','options','head']
    def get_queryset(self):
        return Post.objects.filter(
            Q(channel__type='public') |
            Q(channel__owner=self.request.user) |
            Q(channel__followers__user=self.request.user)
            ).distinct()
    def perform_update(self, serializer):
        if serializer.instance.channel.owner != self.request.user:
            raise PermissionDenied('Only the channel owner can edit posts')
        serializer.save()
    def perform_destroy(self, instance):
        if instance.channel.owner != self.request.user:
            raise PermissionDenied('Only the channel owner can delete posts')
        instance.delete()