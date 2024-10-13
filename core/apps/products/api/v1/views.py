from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from apps.products import models
from . import serializers
from .pagination import StandardResultsSetPagination


class SizeViewSet(ModelViewSet):
    serializer_class = serializers.SizeSerializer
    queryset = models.Size.objects.all()
    authentication_classes = (JWTAuthentication,)
    parser_classes = (MultiPartParser,)
    permission_classes = (IsAdminUser,)
    pagination_class = StandardResultsSetPagination


class ColorViewSet(ModelViewSet):
    serializer_class = serializers.ColorSerializer
    queryset = models.Color.objects.all()
    authentication_classes = (JWTAuthentication,)
    parser_classes = (MultiPartParser,)
    permission_classes = (IsAdminUser,)
    pagination_class = StandardResultsSetPagination


class CategoryViewSet(ModelViewSet):
    serializer_class = serializers.CategorySerializer
    queryset = models.Category.objects.all()
    authentication_classes = (JWTAuthentication,)
    parser_classes = (MultiPartParser,)
    permission_classes = (IsAdminUser,)
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ["is_publish"]
    search_fields = ["name", "slug"]


class BrandViewSet(ModelViewSet):
    serializer_class = serializers.BrandSerializer
    queryset = models.Brand.objects.all()
    authentication_classes = (JWTAuthentication,)
    parser_classes = (MultiPartParser,)
    permission_classes = (IsAdminUser,)
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ["is_publish"]
    search_fields = ["name"]


class OfferViewSet(ModelViewSet):
    serializer_class = serializers.OfferSerializer
    queryset = models.Offer.objects.all()
    authentication_classes = (JWTAuthentication,)
    parser_classes = (MultiPartParser,)
    permission_classes = (IsAdminUser,)
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ["is_publish"]
    search_fields = ["title"]


class ProductViewSet(ModelViewSet):
    serializer_class = serializers.ProductSerializer
    queryset = models.Product.objects.all()
    authentication_classes = (JWTAuthentication,)
    parser_classes = (MultiPartParser,)
    permission_classes = (IsAdminUser,)
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ["is_publish", "gender"]
    search_fields = ["name", "slug"]


class ImageViewSet(ModelViewSet):
    serializer_class = serializers.ImageSerializer
    queryset = models.Image.objects.all()
    authentication_classes = (JWTAuthentication,)
    parser_classes = (MultiPartParser,)
    permission_classes = (IsAdminUser,)
    pagination_class = StandardResultsSetPagination


class AdditionalInformationViewSet(ModelViewSet):
    serializer_class = serializers.AdditionalInformationSerializer
    queryset = models.AdditionalInformation.objects.all()
    authentication_classes = (JWTAuthentication,)
    parser_classes = (MultiPartParser,)
    permission_classes = (IsAdminUser,)
    pagination_class = StandardResultsSetPagination


class ReviewViewSet(ModelViewSet):
    serializer_class = serializers.ReviewSerializer
    queryset = models.Review.objects.all()
    authentication_classes = (JWTAuthentication,)
    parser_classes = (MultiPartParser,)
    permission_classes = (IsAdminUser,)
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["is_valid"]
