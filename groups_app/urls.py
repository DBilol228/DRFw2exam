from django.urls import path
from .views import *

urlpatterns = [
    path('', GroupListCreateView.as_view(), name='group-list-create'),
    path('<int:pk>/', GroupDetailView.as_view(), name='group-detail'),
    path('<int:group_id>/members/', GroupMemberListCreateView.as_view(), name='group-members'),
    path('<int:group_id>/members/me/',LeaveGroupView.as_view(), name='group-leave'),
    path('<int:group_id>/members/<int:pk>/', GroupMemberUpdateView.as_view(), name='group-member-update'),
    path('<int:group_id>/messages/',GroupMessageListCreateView.as_view(), name='group-messages'),
]