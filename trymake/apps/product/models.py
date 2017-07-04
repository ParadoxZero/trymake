"""

Author: Sidhin S Thomas (sidhin@trymake.com)

Copyright (c) 2017 Sibibia Technologies Pvt Ltd
All Rights Reserved

Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential

"""

import decimal
import os

from django.core.files.uploadedfile import UploadedFile
from django.db import models

# Create your models here.
from django.utils.datetime_safe import datetime

from trymake import settings
from trymake.apps.commons.models import Image


class AttributeName(models.Model):
    name = models.CharField(max_length=250, unique=True, db_index=True)


def get_upload_path_product_image(intance: 'Product', filename: str):
    filename, file_extension = os.path.splitext(filename)
    return '{0}{1}{2}'.format(settings.PRODUCT_IMAGE_BASE_URL, intance.slug, file_extension)


def get_upload_path_additional_image(instance: 'AdditionalImages', filename: str):
    filename, file_ext = os.path.splitext(filename)
    return '{0}{1}/{2}{3}'.format(settings.PRODUCT_ADDITIONAL_IMAGES_BASE_URL, instance.product.slug, instance.name,
                                  file_ext)


class Product(models.Model):
    IMAGE_SAVE_URL_BASE = 'assets/product/image/'
    # Serialize Keys
    NAME = 'name'
    SLUG = 'slug'
    WEIGHT = 'weight'
    SHORT_DESCRIPTION = 'short_description'
    DESCRIPTION = 'description'
    COVER_IMAGE_URL = 'cover_image_url'

    name = models.CharField(max_length=250, unique=True, db_index=True)
    slug = models.CharField(max_length=10, unique=True, db_index=True)
    approximate_weight = models.DecimalField(max_digits=6, decimal_places=2)
    short_description = models.TextField()
    description = models.TextField()
    product_image = models.ImageField(upload_to=get_upload_path_product_image)

    @staticmethod
    def get_product_details(product_slug):
        product = Product.objects.prefetch_related('images', 'attributevalues_set',
                                                   'attributevalues_set__attribute').get(slug=product_slug)
        additional_images = product.additional_images.all()
        attributes = product.attributevalues_set.all()
        attribute_details = list()
        for attribute in attributes:
            attribute_details.append({
                'name': attribute.attribute.name,  # type:AttributeValues
                'value': attribute.value,
                'attribute_id': attribute.attribute_id
            })
        return {
            'details': product.serialize,
            'attributes': attribute_details,
            'additional_images': [image.serialize for image in additional_images]
        }

    @property
    def serialize(self):
        return {
            self.NAME: self.name,
            self.SLUG: self.slug,
            self.WEIGHT: self.approximate_weight,
            self.SHORT_DESCRIPTION: self.short_description,
            self.DESCRIPTION: self.description,
            self.COVER_IMAGE_URL: self.product_image.url
        }

    @classmethod
    def create_product(cls, name: str, slug: str, approximate_weight: decimal,
                       short_description: str, long_Description: str,
                       image: UploadedFile) -> 'Product':
        product = cls(name=name, short_description=short_description, description=long_Description,
                      approximate_weight=approximate_weight)
        product.product_image = image
        product.save()

        return product


class AdditionalImages(models.Model):
    name = models.CharField(max_length=250, unique=True, db_index=True)
    image = models.ImageField(upload_to=get_upload_path_additional_image)
    date_added = models.DateTimeField()
    product = models.ForeignKey(Product, to_field='slug')

    @property
    def serialize(self):
        return {
            'name': self.name,
            'image_url': self.image.url
        }


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

    def filter(self, attribute_value_list: list):
        return self.objects.filter(attributes__attributevalues__in=attribute_value_list)

        # TODO def create_category(name, image, parent=None)


class DiscountOffer(models.Model):
    name = models.CharField(max_length=250)
    discount_percent = models.PositiveSmallIntegerField()
    products = models.ManyToManyField(Product)

    @classmethod
    def create(cls, name: str, percentage: int, product_list: list = None):
        discount = cls()
        discount.name = name
        discount.discount_percent = percentage
        discount.save()
        if product_list is not None:
            discount.products.add(*product_list)
