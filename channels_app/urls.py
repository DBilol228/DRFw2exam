from django.urls import path
from .views import *

urlpatterns = [
    path('',ChannelListCreateView.as_view(),name='channel-list-create'),
    path('following/',FollowingListView.as_view(),name='following-list'),
    path('<int:channel_id>/follow/',FollowChannelView.as_view(),name='channel-follow'),
    path('<int:channel_id>/is_following/',IsFollowingView.as_view(),name='channel-is-following'),
    path('<int:channel_id>/posts/',PostListCreateView.as_view(),name='channel-posts'),
    path('posts/<int:pk>/',PostDetailView.as_view(),name='post-detail'),
    path('<int:pk>/',ChannelDetailView.as_view(),name='channel-detail'),
]
