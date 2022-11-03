from django.contrib import admin

from .models import User, Artist
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'email',
        'authority',
    ]


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = [
        'user_nickname',
        'name',
        'gender',
        'birth_date',
        'email',
        'phone_number',
        'check_available',
    ]