from myapp.models import Account
from .models import Group, GroupMember, GroupMessage
from .serializers import GroupSerializer, GroupMemberSerializer, GroupMessageSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

class GroupListCreateView(ListCreateAPIView):
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    def get_queryset(self):
        return Group.objects.filter(members__user=self.request.user).distinct().order_by('-created_at')
    def perform_create(self, serializer):
        group = serializer.save(owner=self.request.user)
        GroupMember.objects.create(group=group,user=self.request.user,role='owner')

class GroupDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    http_method_names = ['patch','delete','options','head']
    def perform_update(self, serializer):
        group = self.get_object()
        member = GroupMember.objects.filter(group=group,user=self.request.user).first()
        if not member or member.role not in ['owner','admin']:
            raise PermissionDenied('Only the owner or admin can edit this group')
        serializer.save()    
    def perform_destroy(self, instance):
        if instance.owner != self.request.user:
            raise PermissionDenied('Only owner can delete the group')
        instance.delete()
    def get_parsers(self):
        if self.request.method == 'PATCH':
            return [MultiPartParser(), FormParser()]
        return super().get_parsers()

class GroupMemberListCreateView(ListCreateAPIView):
    serializer_class = GroupMemberSerializer
    permission_classes = [IsAuthenticated]
    def get_group(self):
        return get_object_or_404(Group,pk=self.kwargs['group_id'])
    def check_number(self,group):
        if not GroupMember.objects.filter(group=group,user=self.request.user).exists():
            raise PermissionDenied('You are not a member of this group')
    def get_queryset(self):
        group = self.get_group()
        self.check_number(group)
        return GroupMember.objects.filter(group=group).order_by('joined_at')
    def perform_create(self, serializer):
        group = self.get_group()
        member = GroupMember.objects.filter(group=group,user=self.request.user).first()
        if not member or member.role not in ['owner','admin']:
            raise PermissionDenied('Only the owner or admin can add members')
        user_id = self.request.data.get('user')
        if not user_id:
            raise ValidationError({'user':'This field is required'})
        user = get_object_or_404(Account,pk=user_id)
        if GroupMember.objects.filter(group=group,user=user).exists():
            raise ValidationError({'user':'This user is already member'})
        serializer.save(group=group,user=user,role='member')

class GroupMemberUpdateView(UpdateAPIView):
    serializer_class = GroupMemberSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['put','patch','options','head']
    def get_queryset(self):
        return GroupMember.objects.filter(group_id=self.kwargs['group_id'])
    def perform_update(self, serializer):
        group = serializer.instance.group
        if group.owner != self.request.user:
            raise PermissionDenied('Only the group owner can change member roles')
        serializer.save()

class LeaveGroupView(DestroyAPIView):
    serializer_class = GroupMemberSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return GroupMember.objects.filter(group_id=self.kwargs['group_id'],user=self.request.user)
    def perform_destroy(self, instance):
        if instance.group.owner==self.request.user or instance.role == 'owner':
            raise ValidationError('The group owner cannot leave the group')
        instance.delete()

class GroupMessageListCreateView(ListCreateAPIView):
    serializer_class = GroupMessageSerializer
    permission_classes = [IsAuthenticated]
    def get_group(self):
        return get_object_or_404(Group,pk=self.kwargs['group_id'])
    def check_number(self,group):
        if not GroupMember.objects.filter(group=group,user=self.request.user).exists():
            raise PermissionDenied('You are not member of this group')
    def get_queryset(self):
        group = self.get_group()
        self.check_number(group)
        return GroupMessage.objects.filter(group=group).order_by('created_at')
    def perform_create(self,serializer):
        group = self.get_group()
        self.check_number(group)
        serializer.save(group=group,author=self.request.user)

class GroupMessageDeleteView(DestroyAPIView):
    queryset = GroupMessage.objects.all()
    serializer_class = GroupMessageSerializer
    permission_classes = [IsAuthenticated]
    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied('You can delete only your own message')
        instance.delete()