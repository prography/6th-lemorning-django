import json

from django.shortcuts import render, get_object_or_404
from rest_framework import generics, viewsets
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser

from .serializers import *
from .models import *
from .apps import ShopConfig
import io
from itertools import chain


def product_in_category(request, category_slug=None):
    current_category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available_display=True)

    if category_slug:
        current_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=current_category)

    return render(request, 'shop/list.html',
                  {'current_category': current_category, 'categories': categories, 'products': products})


def product_detail(request, id, product_slug=None):
    product = get_object_or_404(Product, id=id, slug=product_slug)
    return render(request, 'shop/detail.html', {'product': product})


# 알람을 올리는 API
class productList(generics.CreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        parser_classes = (MultiPartParser,)
        serializer = self.get_serializer(data=request.data)
        data = request.FILES['alarm']
        k = io.BytesIO(data.file.read())
        feat, tag = ShopConfig.model.extract_info(k, mode='both', topN=5)
        ShopConfig.Engine.set_collection('musicRDB')
        taglist = tag.tolist()
        if serializer.is_valid():
            serializer.validated_data['tags'] = taglist
            serializer.save(user=request.user)
            id = serializer.data['id']
            # print(type(id))
            ShopConfig.Engine.insert_data(id, feat)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 알람 첫 페이지 List
class WelcomeProduct(generics.ListAPIView):
    serializer_class = WelcomeProductSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Product.objects.all()

    def list(self, request, *args, **kwargs):
        response = {
            'status': status.HTTP_200_OK,
            'message': "Welcome alarm List",
            'response': super().list(request, *args, **kwargs).data
        }
        return Response(response)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=True, methods=['get'], )
    def recommand_category(self, request, pk):
        ## 추천된 ID의 list여기서 불러오고
        ShopConfig.Engine.set_collection('musicRDB')
        li_id, li_distance = ShopConfig.Engine.search_by_key(int(pk), 5)
        key = list(chain(*li_id))
        ## list의 id 값들 다 빼오고 밑에다가 다 넣어야함.
        qs = self.queryset.filter(pk__in=key)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)


    @action(detail=False, methods=['get'], )
    def weekly_list(self, request):
        qs = self.queryset.order_by('-created')
        serializer = self.get_serializer(qs, many=True)
        response = {
            'status': status.HTTP_200_OK,
            'message': "Category List",
            'response': serializer.data
        }
        return Response(response)