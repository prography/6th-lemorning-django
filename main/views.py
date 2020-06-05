from django.views.generic import ListView
from main.models import Main

# Create your views here.
class MainLV(ListView):
    model = Main