from django.conf import settings
from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = getattr(settings, "PAGE_SIZE", 5)
