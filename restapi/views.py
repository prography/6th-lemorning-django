from django.contrib.auth.models import User, Group
from rest_framework.decorators import action
from rest_framework.response import Response

from accounts.models import Account
from board.models import Board
from shop.models import Product,Category
from rest_framework import viewsets
from rest_framework import permissions
from restapi.serializers import UserSerializer, GroupSerializer,AccountSerializer, BoardSerializer, ProductSerializer,CategorySerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

class BoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    # permission_classes = [permissions.IsAuthenticated]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=True, methods=['get'], )
    def recommand_category(self, request, pk):
        qs = self.queryset.filter(category_id=pk)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'],)
    def weekly_list(self, request):
        qs = self.queryset.order_by('-created')
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer