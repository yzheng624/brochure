from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=200)
    current_price = models.DecimalField(max_digits=10, decimal_places=6)
    original_price = models.DecimalField(max_digits=10, decimal_places=6)
    url = models.URLField()
    status = models.CharField(max_length=200)
    website = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name
