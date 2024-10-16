# Generated by Django 5.1.1 on 2024-10-17 10:42

import autoslug.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Brand",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50, verbose_name="name")),
                (
                    "image_file",
                    models.ImageField(upload_to="brand/images", verbose_name="image"),
                ),
                (
                    "is_publish",
                    models.BooleanField(default=True, verbose_name="is publish"),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="created at"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="updated at"),
                ),
            ],
            options={
                "verbose_name": "Brand",
                "verbose_name_plural": "Brands",
                "ordering": ("-created_at", "-updated_at"),
            },
        ),
        migrations.CreateModel(
            name="Color",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=15, verbose_name="color")),
            ],
            options={
                "verbose_name": "Color",
                "verbose_name_plural": "Colors",
            },
        ),
        migrations.CreateModel(
            name="Offer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=50, verbose_name="title")),
                (
                    "description",
                    models.TextField(blank=True, null=True, verbose_name="description"),
                ),
                (
                    "image_file",
                    models.ImageField(upload_to="offer/images", verbose_name="image"),
                ),
                (
                    "discount_percentage",
                    models.FloatField(verbose_name="discount percentage"),
                ),
                ("start_time", models.DateTimeField(verbose_name="start time")),
                ("end_time", models.DateTimeField(verbose_name="end time")),
                (
                    "is_publish",
                    models.BooleanField(default=True, verbose_name="is publish"),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="created at"),
                ),
            ],
            options={
                "verbose_name": "Offer",
                "verbose_name_plural": "Offers",
                "ordering": ("-discount_percentage", "-start_time"),
            },
        ),
        migrations.CreateModel(
            name="Size",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=15, verbose_name="size")),
            ],
            options={
                "verbose_name": "Size",
                "verbose_name_plural": "Sizes",
            },
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50, verbose_name="name")),
                (
                    "slug",
                    autoslug.fields.AutoSlugField(
                        editable=True,
                        populate_from="name",
                        unique=True,
                        verbose_name="slug",
                    ),
                ),
                (
                    "image_file",
                    models.ImageField(
                        upload_to="products/images", verbose_name="image"
                    ),
                ),
                (
                    "is_publish",
                    models.BooleanField(default=True, verbose_name="is publish"),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="created at"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="updated at"),
                ),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="subs",
                        to="products.category",
                        verbose_name="parent",
                    ),
                ),
            ],
            options={
                "verbose_name": "Category",
                "verbose_name_plural": "Categories",
                "ordering": ("-created_at", "-updated_at"),
            },
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50, verbose_name="name")),
                (
                    "slug",
                    autoslug.fields.AutoSlugField(
                        editable=True,
                        populate_from="name",
                        unique=True,
                        verbose_name="slug",
                    ),
                ),
                (
                    "information",
                    models.CharField(
                        blank=True, max_length=120, verbose_name="information"
                    ),
                ),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2, max_digits=12, verbose_name="price"
                    ),
                ),
                (
                    "quantity",
                    models.PositiveSmallIntegerField(
                        default=0, verbose_name="quantity"
                    ),
                ),
                (
                    "gender",
                    models.CharField(
                        choices=[("M", "Male"), ("F", "Female"), ("K", "Kids")],
                        max_length=1,
                        verbose_name="gender",
                    ),
                ),
                (
                    "is_publish",
                    models.BooleanField(default=True, verbose_name="is publish"),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="created at"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="updated at"),
                ),
                (
                    "brand",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="products",
                        to="products.brand",
                        verbose_name="brand",
                    ),
                ),
                (
                    "category",
                    models.ManyToManyField(
                        related_name="products",
                        to="products.category",
                        verbose_name="category",
                    ),
                ),
                (
                    "color",
                    models.ManyToManyField(
                        related_name="products",
                        to="products.color",
                        verbose_name="color",
                    ),
                ),
                (
                    "likes",
                    models.ManyToManyField(
                        blank=True,
                        related_name="liked_products",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="likes",
                    ),
                ),
                (
                    "offer",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="products",
                        to="products.offer",
                        verbose_name="offer",
                    ),
                ),
                (
                    "size",
                    models.ManyToManyField(
                        related_name="products", to="products.size", verbose_name="size"
                    ),
                ),
            ],
            options={
                "verbose_name": "Product",
                "verbose_name_plural": "Products",
                "ordering": ("-created_at", "-price"),
            },
        ),
        migrations.CreateModel(
            name="Image",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image_file",
                    models.ImageField(
                        upload_to="products/images", verbose_name="image"
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="products.product",
                        verbose_name="product",
                    ),
                ),
            ],
            options={
                "verbose_name": "Image",
                "verbose_name_plural": "Images",
            },
        ),
        migrations.CreateModel(
            name="AdditionalInformation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "additional_details",
                    models.TextField(verbose_name="additional details"),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="additional_infos",
                        to="products.product",
                        verbose_name="product",
                    ),
                ),
            ],
            options={
                "verbose_name": "Additional Information",
                "verbose_name_plural": "Additional Informations",
            },
        ),
        migrations.CreateModel(
            name="Review",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.CharField(max_length=120, verbose_name="text")),
                (
                    "is_valid",
                    models.BooleanField(default=True, verbose_name="is valid"),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="created at"),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reviews",
                        to="products.product",
                        verbose_name="product",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reviews",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="user",
                    ),
                ),
            ],
            options={
                "verbose_name": "Review",
                "verbose_name_plural": "Reviews",
                "ordering": ("-created_at",),
            },
        ),
    ]
