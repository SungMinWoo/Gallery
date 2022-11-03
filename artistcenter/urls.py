from django.urls import path

from .views import *


appname = 'artistcenter'

urlpatterns = [
    path('', artistcenter, name='artistcenter'),
    path('exhibit/list', exhibit_list, name='exhibit_list'),
    path('artist/product/list', artist_product_list, name='artist_product_list'),
    path('artist/list', artist_list, name='artist_list'),
    path('product/list', product_list, name='product_list'),
]