from rest_framework import serializers
from apps.orders import models


class ProvinceSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Province
        fields = "__all__"


class CitySerializers(serializers.ModelSerializer):
    class Meta:
        model = models.City
        fields = "__all__"


class AddressSerializers(serializers.ModelSerializer):

    class Meta:
        model = models.Address
        fields = "__all__"




class OrderSerializers(serializers.ModelSerializer):

    class Meta:
        model = models.Order
        fields = "__all__"




class OrderItemSerializers(serializers.ModelSerializer):

    class Meta:
        model = models.OrderItem
        fields = "__all__"