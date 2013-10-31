from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=6)

    def __unicode__(self):
        return self.name

class Company(models.Model):
    pass