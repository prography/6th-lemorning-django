from django.apps import AppConfig
from deep.model import DeepModel
from deep.search_engine.milvusdb import SearchEngine


class ShopConfig(AppConfig):
    name = 'shop'
    model = DeepModel()
    Engine = SearchEngine('3.129.97.14', 19530)