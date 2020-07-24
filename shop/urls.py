from django.urls import path,include
from .views import *
from rest_framework import routers

app_name = 'shop'


router = routers.DefaultRouter()
router.register('', ProductViewSet)

urlpatterns = [
    path('',product_in_category,name='product_all'),
    # path('<slug:category_slug>/',product_in_category,name='product_in_category'),
    path('<int:id>/<product_slug>/',product_detail,name='product_detail'),
    path('product', productList.as_view()),
    path('welcome', WelcomeProduct.as_view()),
    path('lists/', include(router.urls))
]