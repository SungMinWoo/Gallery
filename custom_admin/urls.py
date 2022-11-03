from django.urls import path
from .views import *
app_name = 'custom_admin'

urlpatterns = [
    path('', custom_admin, name='custom_admin'),
    path('approval', admin_approval, name='approval'),
    path('disapproval', admin_disapproval, name='disapproval'),
    path('regist/confirm', custom_admin, name='confirm'),
    path('stats', artist_stats, name='artist_stats')
]