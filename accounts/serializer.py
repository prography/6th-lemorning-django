from rest_framework import serializers, status
from rest_auth.registration.serializers import RegisterSerializer

from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['profile', 'nickname','sex', 'birth']


class RegisterSerializer(RegisterSerializer):

    account = AccountSerializer()
    email = serializers.EmailField()
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def get_cleaned_data(self):
        add ={'sex': self.validated_data.get("account", '')['sex'],
              'profile': self.validated_data.get("account", '')['profile'],
              'nickname': self.validated_data.get("account", '')['nickname'],
              'birth': self.validated_data.get("account", '')['birth'],
              }
        result = {**super().get_cleaned_data(), **add}
        return  result

    def save(self, request):
        return super().save(request)
