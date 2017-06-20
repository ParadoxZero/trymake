from django.db import models


# Create your models here.


class AttributeName(models.Model):
    name = models.CharField(max_length=500, unique=True, db_index=True)


class AttributeValues(models.Model):
    attribute = models.ForeignKey(AttributeName)
    value = models.CharField(max_length=500)


class Image(models.Model):
    upload_to = models.CharField(max_length=100)
    name = models.CharField(max_length=500, unique=True, db_index=True)
    image = models.ImageField(upload_to=upload_to, name=name)
    date_added = models.DateTimeField()

    # TODO def create(upload_to, name, image, date)
    # TODO def delete_image()


class Product(models.Model):
    name = models.CharField(max_length=500, unique=True, db_index=True)
    sku = models.CharField(max_length=4, unique=True, db_index=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    discount = models.PositiveSmallIntegerField(null=True, default=0)
    attribute_value = models.OneToOneField(AttributeValues)

    # TODO def create(name:str,sku:str,price:str, attribute_list:dictionary)


class Category(models.Model):
    name = models.CharField(max_length=500, unique=True, db_index=True)
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
