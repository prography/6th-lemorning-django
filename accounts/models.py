from django.db import models
from django.contrib.auth.models import User

from config.storage_backends import PrivateMediaStorage

Sex_Choices = (('male', '남성'), ('Female', '여성'))
Social_Choices = (('NAVER', 'naver'), ('GOOGLE', 'google'),
                  ('KAKAO', 'kakao'),('NONE', 'none'))

# Create your models here.
class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile = models.ImageField(upload_to='Accoount_Profile/%Y/%m/%d',blank=True, default="default-profile.jpg",storage=PrivateMediaStorage())
    nickname = models.CharField(max_length=40, blank=True, null=True)
    social = models.CharField(max_length=30, choices=Social_Choices, default="NONE", blank=True, null=True)
    sex = models.CharField(max_length=15, choices=Sex_Choices)
    birth = models.DateField(null=True)
    wallet = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username