from django.contrib.auth.models import User, Group
from accounts.models import Account
from rest_framework import serializers
from board.models import Board
from shop.models import Product, Category
from taggit_serializer.serializers import TaggitSerializer,TagListSerializerField


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



class BoardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Board
        fields = ['id', 'title', 'alarm', 'create_date', ]


class ProductSerializer(TaggitSerializer, serializers.HyperlinkedModelSerializer):
    tags = TagListSerializerField()

    category_no = serializers.SerializerMethodField()
    category_name = serializers.SlugField(source='category')

    def get_category_no(self, obj):
        return obj.category.id

    class Meta:
        model = Product
        fields = ['id', 'name', 'category_no', 'category_name', 'image', 'alarm', 'tags' ]


class ProductsSerializer(serializers.HyperlinkedModelSerializer):
    category_no = serializers.SerializerMethodField()
    category_name = serializers.SlugField(source='category')

    def get_category_no(self, obj):
        return obj.category.id

    class Meta:
        model = Product
        fields = ['id', 'name','category', 'category_no', 'category_name', 'image', 'alarm', ]
        # depth = 2

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['name']
