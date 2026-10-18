from django.urls import path
from .views import RegisterView,TokenView,MeView,ChangePasswordView
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', TokenView.as_view(), name='token'),
    path('me/', MeView.as_view(), name='me'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
]