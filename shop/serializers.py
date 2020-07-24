from rest_framework import serializers
from taggit_serializer.serializers import TaggitSerializer, TagListSerializerField
from .models import Product



class ProductSerializer(TaggitSerializer, serializers.HyperlinkedModelSerializer):

    tags = TagListSerializerField()
    #
    # category_no = serializers.SerializerMethodField()
    # category_name = serializers.SlugField(source='category')
    #
    # def get_category_no(self, obj):
    #     return obj.category.id


    class Meta:
        model = Product
        # fields = ['id', 'name', 'category_no', 'category_name', 'image', 'alarm', 'tags' ]
        fields = ['id', 'name', 'image', 'alarm', 'price', 'stock', 'tags']


class WelcomeProductSerializer(TaggitSerializer, serializers.HyperlinkedModelSerializer):
    tags = TagListSerializerField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'image', 'tags']