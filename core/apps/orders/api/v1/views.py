from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from apps.orders import models
from . import serializers
from .pagination import StandardResultsSetPagination


class ProvinceView(ModelViewSet):
    serializer_class = serializers.ProvinceSerializers
    queryset = models.Province.objects.all()
    authentication_classes = (JWTAuthentication,)
    parser_classes = (MultiPartParser,)
    permission_classes = (IsAdminUser,)


class CityView(ModelViewSet):
    serializer_class = serializers.CitySerializers
    queryset = models.City.objects.all()
    parser_classes = (MultiPartParser,)
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminUser,)


class AddressView(ModelViewSet):
    serializer_class = serializers.AddressSerializers
    queryset = models.Address.objects.all()
    authentication_classes = (JWTAuthentication,)
    parser_classes = (MultiPartParser,)
    permission_classes = (IsAdminUser,)
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ["is_active"]
    search_fields = [
        "user__phone",
        "user__username",
        "recipient_name",
        "recipient_phone_number",
    ]


class OrderView(ModelViewSet):
    serializer_class = serializers.OrderSerializers
    queryset = models.Order.objects.all()
    authentication_classes = (JWTAuthentication,)
    parser_classes = (MultiPartParser,)
    permission_classes = (IsAdminUser,)
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ["is_paid"]
    search_fields = ["user__phone", "user__username"]


class OrderItemView(ModelViewSet):
    serializer_class = serializers.OrderItemSerializers
    queryset = models.OrderItem.objects.all()
    authentication_classes = (JWTAuthentication,)
    parser_classes = (MultiPartParser,)
    permission_classes = (IsAdminUser,)
    filter_backends = [filters.SearchFilter]
    search_fields = ["product__name", "product__slug"]
