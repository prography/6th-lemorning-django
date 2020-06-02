from django.contrib.auth.models import User, Group
from accounts.models import Account
from rest_framework import serializers
from board.models import Board
from shop.models import Product, Category


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'last_name', 'first_name', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class AccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Account
        fields = ['url', 'user', 'sex', 'wallet']


class BoardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Board
        fields = ['id', 'title', 'alarm', 'create_date', ]


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    category_no = serializers.SerializerMethodField()
    category_name = serializers.SlugField(source='category')

    def get_category_no(self, obj):
        return obj.category.id

    class Meta:
        model = Product
        fields = ['id', 'name', 'category_no', 'category_name', 'image', 'alarm', ]


class ProductsSerializer(serializers.HyperlinkedModelSerializer):
    category_no = serializers.SerializerMethodField()
    category_name = serializers.SlugField(source='category')

    def get_category_no(self, obj):
        return obj.category.id

    class Meta:
        model = Product
        fields = ['id', 'name','category', 'category_no', 'category_name', 'image', 'alarm']
        # depth = 2

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['name']