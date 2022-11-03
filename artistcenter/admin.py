from django.contrib import admin

# Register your models here.
from .models import Product, Exhibit
# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'price',
        'artist',
    ]


@admin.register(Exhibit)
class ExhibitAdmin(admin.ModelAdmin):
    list_display = [
        'artist_exhibit',
        'exhibit_title',
    ]
