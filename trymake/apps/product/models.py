"""

Author: Sidhin S Thomas (sidhin@trymake.com)

Copyright (c) 2017 Trymake Inc
All Rights Reserved
Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential
"""

import decimal
from django.core.files.uploadedfile import UploadedFile
from django.db import models

# Create your models here.
from django.utils.datetime_safe import datetime

from trymake.apps.commons.models import Image


class AttributeName(models.Model):
    name = models.CharField(max_length=250, unique=True, db_index=True)


class Product(models.Model):
    name = models.CharField(max_length=250, unique=True, db_index=True)
    slug = models.CharField(max_length=4, unique=True, db_index=True)
    approximate_weight = models.DecimalField(max_digits=6, decimal_places=2)
    short_description = models.TextField()
    description = models.TextField()
    cover_image = models.ForeignKey(Image,related_name="cover_image")
    images = models.ManyToManyField(Image, related_name="additional_images")

    @classmethod
    def create_product(cls,name: str, slug: str, approximate_weight: decimal,
                           short_description: str, long_Description: str,
                           image: UploadedFile, image_name: str)->"Product":
        product = cls(name=name, short_description=short_description, description=long_Description,
                      approximate_weight=approximate_weight)
        product.save()
        image = Image(name=image_name, date_added=datetime.now())
        image.image = image
        image.save()
        product.images.add(image)
        return product


class AttributeValues(models.Model):
    attribute = models.ForeignKey(AttributeName)
    value = models.CharField(max_length=500)
    product = models.ForeignKey(Product)

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

    def filter(self,attribute_value_list:list):
        return self.objects.filter(attributes__attributevalues__in=attribute_value_list)

        # TODO def create_category(name, image, parent=None)


class DiscountOffer(models.Model):
    name = models.CharField(max_length=250)
    discount_percent = models.PositiveSmallIntegerField()
    products = models.ManyToManyField(Product)

    def add_products(self,product_list):
        self.products.add(*[product.pk for product in product_list])

    @classmethod
    def create(cls,name:str,percentage:int,product_list:list=None):
        discount = cls()
        discount.name = name
        discount.discount_percent = percentage
        discount.save()
        if product_list is not None:
            discount.add_products(product_list)
