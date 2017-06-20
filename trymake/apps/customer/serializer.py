from rest_framework import serializers

from trymakeAPI.API_1_0.mod_customer import Customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'