from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.db import models

STATUS_CHOICES = (
    ('0', 'not ordered'),
    ('1', 'under confirmation'),
    ('2', 'in progress'),
    ('3', 'in delivery'),
    ('4', 'delivered')
)

class Catalog(models.Model):
    catalog_name = models.CharField(max_length=56, blank=False)
    catalog_link = models.CharField(max_length=56, blank=False, null=False)
    catalog_image = models.ImageField(upload_to='catalogs/', null=True, blank=True)
    catalog_description = models.TextField(max_length=512, blank = True)

    def __str__(self):
        return f"{self.catalog_name}"


class Product(models.Model):
    # catalog = models.ForeignKey(Catalog, related_name='products', on_delete=models.CASCADE)
    catalog = models.ManyToManyField(Catalog, related_name='product')
    item_name = models.CharField(max_length=32, blank=False)
    # item_image = models.OneToOneField(Gallery)
    # item_image = models.ImageField(upload_to='items/img/%Y-%m-%d/', null=False, blank=False)
    item_description = models.TextField(max_length=1512, blank=True)
    item_cost = models.FloatField(blank=True, default=0.0)
    item_link = models.CharField(unique=True, db_index=True, max_length=56, blank=False, null=False)

    def __str__(self):
        return f"{self.item_name}"


class Bracket(models.Model):
    class StatusChoices(models.IntegerChoices):
        user_side=0
    user = models.ForeignKey(User, related_name='bracket', blank=False, on_delete=models.CASCADE)
    products = models.ForeignKey(Product, related_name='product', blank=False, on_delete=models.CASCADE)
    item_number = models.IntegerField(blank=False, default=0)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default='0')

    def __str__(self):
        return f"{self.products}"


class Gallery(models.Model):
    products = models.ForeignKey(Product, related_name='gallery', on_delete=models.CASCADE)
    item_image = models.ImageField(upload_to='gallery/img/%Y-%m-%d/', null=False, blank=False)
    item_description = models.TextField(max_length=1512, blank=True)
    main_image = models.BooleanField(default=False)
    # main_image = models.OneToOneField(Product, on_delete=models.DO_NOTHING)
    def __str__(self):
        return f"{self.products}"

class User(User):
    phone_number = models.CharField(max_length=32, blank=False, default='+7(999)-999-1111')
    # first_name = super.first_name(default='noname')
    def __str__(self):
        if self.first_name: return f"{self.first_name}"
        else: return super.__str__(self)

