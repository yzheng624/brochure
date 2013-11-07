from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=200)
    current_price = models.DecimalField(max_digits=10, decimal_places=6)
    original_price = models.DecimalField(max_digits=10, decimal_places=6)
    url = models.URLField()
    error = models.BooleanField()
    last_update = models.DateTimeField(auto_now=True)
    website = models.CharField(max_length=100)
    uuid = models.CharField(max_length=100)
    type = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class Watchlist(models.Model):
    product = models.ForeignKey(Product)
    user = models.ForeignKey(User)
    desire_price = models.DecimalField(max_digits=10, decimal_places=6)
    mark = models.BooleanField(default=True)

    def __unicode__(self):
        return self.product.name + ' ' + str(self.desire_price)