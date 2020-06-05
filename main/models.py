from django.db import models
from django.urls import reverse

# Create your models here.
class Main(models.Model):
    title = models.CharField("TITLE", max_length=100, blank=True)
    url = models.URLField("URL", unique=False)

    def __str__(self):
        return self.title