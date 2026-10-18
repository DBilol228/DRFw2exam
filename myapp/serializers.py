from rest_framework import serializers
from .models import Account

class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)
    class Meta:
        model = Account
        fields = ['id','phone_number','password']
    def create(self, validated_data):
        phone_number = validated_data['phone_number']
        password = validated_data['password']
        account = Account(username=phone_number,phone_number=phone_number)
        account.set_password(password)
        account.save()
        return account

class TokenSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)