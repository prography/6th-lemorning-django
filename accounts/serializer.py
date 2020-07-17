from rest_framework import serializers, status
from rest_auth.registration.serializers import RegisterSerializer

from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['nickname','sex', 'birth']

class AccountPicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['profile']

class RegisterSerializer(RegisterSerializer):

    account = AccountSerializer()
    email = serializers.EmailField()
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    profile = serializers.ImageField(allow_empty_file=True, default="default-profile.jpg")

    def get_cleaned_data(self):
        add ={'sex': self.validated_data.get("account", '')['sex'],
                'profile': self.validated_data.get("profile", ''),
              'nickname': self.validated_data.get("account", '')['nickname'],
              'birth': self.validated_data.get("account", '')['birth'],
              }
        result = {**super().get_cleaned_data(), **add}
        return result
