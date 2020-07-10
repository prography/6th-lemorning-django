from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from restapi.serializers import *
from .models import *


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
        if serializer.is_valid():
            serializer.save(user=request.user)
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
