from rest_framework.viewsets import ModelViewSet
from . import serializers
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAdminUser
from .pagination import StandardResultsSetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.contrib.auth import get_user_model

User = get_user_model()


class UserViewSet(ModelViewSet):
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()
    authentication_classes = (JWTAuthentication,)
    parser_classes = (MultiPartParser,)
    permission_classes = (IsAdminUser,)
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ["is_active", "is_superuser"]
    search_fields = ["phone", "username", "email"]
