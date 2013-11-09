from django.db import models
from django.contrib.auth.models import User
from jsonfield import JSONField


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
    json = JSONField()

    def __unicode__(self):
        return self.name


class Watchlist(models.Model):
    product = models.ForeignKey(Product)
    user = models.ForeignKey(User)
    desire_price = models.DecimalField(max_digits=10, decimal_places=6)
    mark = models.BooleanField(default=True)
    email = models.EmailField()

    def __unicode__(self):
        return self.product.name + ' ' + str(self.desire_price)


class Setting(models.Model):
    user = models.ForeignKey(User)
    per_product = models.IntegerField(default=60)
    per_round = models.IntegerField(default=60)
    amount = models.DecimalField(default=99.99, decimal_places=4, max_digits=10)
    percent = models.DecimalField(default=0.8, decimal_places=4, max_digits=10)

    def __unicode__(self):
        return self.user.username