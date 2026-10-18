from django.urls import path
from .views import *

urlpatterns = [
    path('',ProfileListView.as_view(), name='profile-list'),
    path('me/',MyProfileView.as_view(), name='my-profile'),
    path('<int:pk>/',ProfileDetailView.as_view(), name='profile-detail'),
    path('avatars/',AvatarCreateView.as_view(), name='avatar-create'),
    path('avatars/<int:pk>/',AvatarDetailView.as_view(), name='avatar-detail'),
]