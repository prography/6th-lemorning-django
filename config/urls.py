"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers
from restapi import views

from config.views import HomeView

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register('account', views.AccountViewSet)
router.register('board', views.BoardViewSet)
router.register('shop', views.ProductViewSet)
# router.register('shops', views.ProductsViewSet)
router.register('category', views.CategoryViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('board/', include('board.urls')),
    path('shop/', include('shop.urls')),
    path('',HomeView.as_view(), name='home'),
    path('account/', include('accounts.urls')),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/', include(router.urls)),
    #### social login 시작 ####
    path('accounts/',include('allauth.urls')),
    path('', include('social_django.urls', namespace='social')),
    path('rest-auth/', include('rest_auth.urls')), # Login, Logout 관련 기능
    path('rest-auth/registration/', include('rest_auth.registration.urls')),  # SignUp 관련 기능
    #### social login 끝 ####
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
