from django.db import models


class User(models.Model):
    nickname = models.CharField(max_length=20, null=True, unique=True)
    email = models.EmailField(max_length=150, null=True, unique=True)
    password = models.CharField(max_length=200, null=False)
    AUTHORITY = (
        ('U', '유저'),
        ('A', '작가'),
        ('M', '관리자'),
    )
    authority = models.CharField(max_length=1, null=False, choices=AUTHORITY, default='U') # 권한

    class Meta:
        db_table = 'user'


class Artist(models.Model):
    user_nickname = models.ForeignKey(User, on_delete=models.CASCADE, related_name='artist')
    name = models.CharField(max_length=16, null=False, unique=False)
    GENDERS = (
        ('M', '남성'),
        ('W', '여성'),
    )
    gender = models.CharField(max_length=1, null=False,choices=GENDERS)
    birth_date = models.DateField(null=False)
    email = models.EmailField(max_length=150, null=True, unique=True)
    phone_number = models.CharField(max_length=15, null=False)
    CHECK_AVAILABLE = (
        ('P', '승인'),
        ('W', '대기'),
        ('N', '불가'),
    )
    check_available = models.CharField(max_length=1, null=False, choices=CHECK_AVAILABLE, default='W')
    joindate = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = 'artist'
