from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from accounts.models import User


class Product(models.Model):
    artist = models.ForeignKey(User, on_delete=models.CASCADE, related_name='artist_product')
    title = models.CharField(max_length=70, null=False)
    price = models.PositiveIntegerField(null=False)
    size = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(500)])
    photo = models.ImageField(upload_to='photos/', default="media/logo.png")
    createdate = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = 'product'

    def __str__(self):
        return str(self.title)

class Exhibit(models.Model):
    artist_exhibit = models.ForeignKey(User, on_delete=models.CASCADE, related_name='artist_exhibit')
    exhibit_title = models.CharField(max_length=60, null=False)
    start_date = models.DateTimeField(null=False)
    end_date = models.DateTimeField(null=False)
    exhibit_list = models.ManyToManyField(Product)


    class Meta:
        db_table = 'exhibit'