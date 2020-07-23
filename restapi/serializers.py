from django.contrib.auth.models import User, Group
from accounts.models import Account
from rest_framework import serializers
from shop.models import Product, Category


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['sex', 'wallet']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    account = AccountSerializer()

    class Meta:
        model = User
        fields = ['url', 'username', 'last_name', 'first_name', 'email', 'groups', 'account']


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['name']
