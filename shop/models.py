from django.db import models
from django.core.validators import FileExtensionValidator
from django.urls import reverse
from taggit.managers import TaggableManager


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200,db_index=True)
    meta_description = models.TextField(blank=True)

    slug = models.SlugField(max_length=200,db_index=True, unique=True, allow_unicode=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_in_category',args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category,on_delete=models.SET_NULL, null=True, related_name='products')
    name = models.CharField(max_length=200,db_index=True)
    slug = models.SlugField(max_length=200,db_index=True, unique=True, allow_unicode=True)

    image = models.ImageField(upload_to='product/%Y/%m/%d',blank=True)
    alarm = models.FileField(blank=True, upload_to="alarm/%Y/%m/%d",
                             validators=[FileExtensionValidator(allowed_extensions=['mp3'])])
    description = models.TextField(blank=True)
    meta_description = models.TextField(blank=True)

    price = models.DecimalField(max_digits=10,decimal_places=2)
    stock = models.PositiveIntegerField()

    available_display = models.BooleanField('Display',default=True) # 상품 판매 유무
    available_order = models.BooleanField('Order', default=True)    # 상품 주문 가능 여부

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    tags = TaggableManager()

    class Meta:
        ordering = ['-created']
        index_together = [['id','slug']]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail',args=[self.id,self.slug])