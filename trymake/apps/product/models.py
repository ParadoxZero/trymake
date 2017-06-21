from django.db import models


# Create your models here.
from trymake.apps.commons.models import Image


class AttributeName(models.Model):
    name = models.CharField(max_length=250, unique=True, db_index=True)


class AttributeValues(models.Model):
    attribute = models.ForeignKey(AttributeName)
    value = models.CharField(max_length=500)


class Product(models.Model):
    name = models.CharField(max_length=250, unique=True, db_index=True)
    sku = models.CharField(max_length=4, unique=True, db_index=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    discount = models.PositiveSmallIntegerField(null=True, default=0)
    approximate_weight = models.DecimalField(max_digits=6,decimal_places=2)
    attribute_value = models.OneToOneField(AttributeValues)
    short_description = models.TextField()
    description = models.TextField()
    images = models.ManyToManyField(Image)

    # TODO def create(name:str,sku:str,price:str, attribute_list:dictionary)


class Category(models.Model):
    name = models.CharField(max_length=250, unique=True, db_index=True)
    image = models.ForeignKey(Image)
    parent_category = models.ForeignKey("self", null=True)
    attributes = models.ManyToManyField(AttributeName)
    products = models.ManyToManyField(Product)

    def get_filters(self):
        attribute_list = self.attributes.all()
        filters = dict()
        for attribute in attribute_list:
            filters[attribute.name] = list(AttributeValues.objects.filter(attribute=attribute).distinct())

        return filters

    # TODO def create_category(name, image, parent=None)
