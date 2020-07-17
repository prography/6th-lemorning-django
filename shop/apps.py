from django.apps import AppConfig
from deep.model import DeepModel



class ShopConfig(AppConfig):
    name = 'shop'
    model = DeepModel()