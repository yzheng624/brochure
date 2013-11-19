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


class Page(models.Model):
    user = models.ForeignKey(User)
    url = models.URLField()
    description = models.CharField(max_length=1000)
    error = models.BooleanField()
    last_update = models.DateTimeField(auto_now=True)
    least_price = models.DecimalField(max_digits=10, decimal_places=6, blank=True)
    discount = models.DecimalField(max_digits=10, decimal_places=6, blank=True)
    email = models.CharField(max_length=10000, blank=True)
    store_name = models.CharField(max_length=100)
    mark = models.BooleanField(default=True)
    product = models.ManyToManyField(Product)
    type = models.CharField(max_length=100)

    def __unicode__(self):
        return self.description


class Watchlist(models.Model):
    product = models.ForeignKey(Product)
    user = models.ForeignKey(User)
    desire_price = models.DecimalField(max_digits=10, decimal_places=6)
    mark = models.BooleanField(default=True)
    email = models.CharField(max_length=10000)

    def __unicode__(self):
        return self.product.name + ' ' + str(self.desire_price)


class Setting(models.Model):
    user = models.ForeignKey(User)
    product = models.IntegerField(default=60)
    round = models.IntegerField(default=60)
    amount = models.DecimalField(default=25, decimal_places=4, max_digits=10)
    percent = models.DecimalField(default=0.9, decimal_places=4, max_digits=10)

    def __unicode__(self):
        return self.user.username
