from django.db import models
from django.contrib.auth.models import User

Sex_Choices = (
    ('male', '남성'),
    ('Female', '여성')
)

# Create your models here.
class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(null=True)
    sex = models.CharField(max_length=15, choices=Sex_Choices)
    wallet = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username