import django_filters
from . import models
from django.utils import timezone


class ProductFilter(django_filters.FilterSet):

    q = django_filters.CharFilter(
        field_name="name", lookup_expr="icontains", label="search"
    )

    gender = django_filters.ChoiceFilter(
        choices=[("M", "Male"), ("F", "Female"), ("K", "Kids")],
        field_name="gender",
        label="gender",
    )

    category = django_filters.ModelMultipleChoiceFilter(
        queryset=models.Category.objects.filter(is_publish=True),
        field_name="category__slug",
        to_field_name="slug",
        label="category",
        distinct=True,
    )

    color = django_filters.ModelMultipleChoiceFilter(
        queryset=models.Color.objects.all(),
        field_name="color__name",
        to_field_name="name",
        label="color",
        distinct=True,
    )

    size = django_filters.ModelMultipleChoiceFilter(
        queryset=models.Size.objects.all(),
        field_name="size__name",
        to_field_name="name",
        label="size",
        distinct=True,
    )

    offer = django_filters.ModelChoiceFilter(
        queryset=models.Offer.objects.filter(
            is_publish=True,
            start_time__lte=timezone.now(),
            end_time__gte=timezone.now(),
        ),
        label="offer",
    )

    price = django_filters.RangeFilter()

    class Meta:
        model = models.Product
        fields = ["q", "category", "gender", "color", "size", "offer", "price"]

    def __init__(self, data=None, queryset=None, *, request=None, prefix=None):
        if queryset is None:
            queryset = models.Product.objects.filter(is_publish=True)

        super().__init__(data, queryset, request=request, prefix=prefix)
