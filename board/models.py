from django.conf import settings
from django.db import models
from django.utils import timezone


# Create your models here.
class Board(models.Model):
    title = models.CharField(max_length=300)
    alarm = models.FileField(blank=True, upload_to="alarm/%Y/%m/%d")
    create_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
