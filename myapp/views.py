from .models import Account
from .serializers import AccountSerializer,TokenSerializer,ChangePasswordSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.status import HTTP_400_BAD_REQUEST,HTTP_401_UNAUTHORIZED,HTTP_200_OK
from rest_framework.generics import CreateAPIView
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterView(CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [AllowAny]

class TokenView(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(request_body=TokenSerializer)
    def post(self,request):
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')
        if not phone_number or not password:
            return Response({'error':'Phone number and password are required'},status=HTTP_400_BAD_REQUEST)
        user = authenticate(request,phone_number=phone_number,password=password)
        if user is None:
            return Response({'error':'Invalid phone number and password'},status=HTTP_401_UNAUTHORIZED)
        refresh = RefreshToken.for_user(user)
        return Response({'refresh':str(refresh),'access':str(refresh.access_token)},status=HTTP_200_OK)

class MeView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        serializer = AccountSerializer(request.user)
        return Response(serializer.data)

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(request_body=ChangePasswordSerializer)
    def post(self,request):
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        if not old_password or not new_password:
            return Response({'error':'Both old password and new password is required'},status=HTTP_400_BAD_REQUEST)
        if not request.user.check_password(old_password):
            return Response({'error':'Old password is incorrect'},status=HTTP_400_BAD_REQUEST)
        try:
            validate_password(new_password,request.user)
        except ValidationError as error:
            return Response({'error':error.messages},status=HTTP_400_BAD_REQUEST)
        request.user.set_password(new_password)
        request.user.save()
        return Response({'message':'Password changed successfully'},status=HTTP_200_OK)