from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Catalog, Product, Gallery, Bracket

admin.site.site_header = "Авто Магазин"
admin.site.site_title = "Авто Магазин"
admin.site.index_title = "Авто Магазин панель Администратора"

@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):
    list_display = ['id', 'catalog_name', 'catalog_link']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'item_name']


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ['id', 'products']


@admin.register(Bracket)
class BracketAdmin(admin.ModelAdmin):
    list_display = ['user', 'products', 'status']