from django.db import models
from django.utils.translation import gettext_lazy as _
from autoslug import AutoSlugField
from django.utils.html import format_html
from django.utils import timezone
from django.utils.text import Truncator
from django.contrib.auth import get_user_model


User = get_user_model()


class Size(models.Model):
    name = models.CharField(_("size"), max_length=15)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Size")
        verbose_name_plural = _("Sizes")


class Color(models.Model):
    name = models.CharField(_("color"), max_length=15)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Color")
        verbose_name_plural = _("Colors")


class Category(models.Model):
    name = models.CharField(_("name"), max_length=50)
    slug = AutoSlugField(_("slug"), populate_from="name", editable=True, unique=True)
    image_file = models.ImageField(_("image"), upload_to="products/images")
    parent = models.ForeignKey(
        "self",
        verbose_name=_("parent"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="subs",
    )
    is_publish = models.BooleanField(_("is publish"), default=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("-created_at", "-updated_at")
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


class Brand(models.Model):
    name = models.CharField(_("name"), max_length=50)
    image_file = models.ImageField(_("image"), upload_to="brand/images")
    is_publish = models.BooleanField(_("is publish"), default=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    def show_image(self):
        return format_html(
            f"<image src='{self.image_file.url}' width='50px' height='50'>"
        )

    show_image.short_description = _("image")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("-created_at", "-updated_at")
        verbose_name = _("Brand")
        verbose_name_plural = _("Brands")


class Offer(models.Model):

    title = models.CharField(_("title"), max_length=50)
    description = models.TextField(_("description"), null=True, blank=True)
    image_file = models.ImageField(_("image"), upload_to="offer/images")
    discount_percentage = models.FloatField(_("discount percentage"))
    start_time = models.DateTimeField(_("start time"))
    end_time = models.DateTimeField(_("end time"))
    is_publish = models.BooleanField(_("is publish"), default=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)

    @property
    def is_active(self):
        now = timezone.now()
        return self.is_publish and now >= self.start_time and now <= self.end_time

    def apply_discount(self, product):
        return float(product.price) * (1 - self.discount_percentage / 100)

    def __str__(self):
        return f"{self.title} ({self.discount_percentage}%)"

    class Meta:
        ordering = ("-discount_percentage", "-start_time")
        verbose_name = _("Offer")
        verbose_name_plural = _("Offers")


class Product(models.Model):

    GENDER_CHOICES = (("M", _("Male")), ("F", _("Female")), ("K", _("Kids")))

    name = models.CharField(_("name"), max_length=50)
    slug = AutoSlugField(_("slug"), populate_from="name", editable=True, unique=True)
    information = models.CharField(_("information"), max_length=120, blank=True)

    price = models.DecimalField(_("price"), max_digits=12, decimal_places=2)
    quantity = models.PositiveSmallIntegerField(_("quantity"), default=0)
    gender = models.CharField(_("gender"), max_length=1, choices=GENDER_CHOICES)

    category = models.ManyToManyField(
        Category, verbose_name=_("category"), related_name="products"
    )
    color = models.ManyToManyField(
        Color, verbose_name=_("color"), related_name="products"
    )
    size = models.ManyToManyField(Size, verbose_name=_("size"), related_name="products")
    likes = models.ManyToManyField(
        User, blank=True, verbose_name=_("likes"), related_name="liked_products"
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("brand"),
        related_name="products",
    )
    offer = models.ForeignKey(
        Offer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("offer"),
        related_name="products",
    )

    is_publish = models.BooleanField(_("is publish"), default=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    @property
    def formatted_price(self):
        return f"{self.price:,.2f}"

    def __str__(self):
        return f"{self.name} - {self.price} {self.brand.name if self.brand else ''}"

    class Meta:
        ordering = ("-created_at", "-price")
        verbose_name = _("Product")
        verbose_name_plural = _("Products")


class Image(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_("product"),
        related_name="images",
    )
    image_file = models.ImageField(_("image"), upload_to="products/images")

    def show_image(self):
        return format_html(
            f"<image src='{self.image_file.url}' width='50px' height='50'>"
        )

    show_image.short_description = _("image")

    def __str__(self):
        return f"{self.product.name}: {self.image_file.name.split('/')[-1]}"

    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Images")


class AdditionalInformation(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_("product"),
        related_name="additional_infos",
    )
    additional_details = models.TextField(_("additional details"))

    def __str__(self):
        truncated_description = Truncator(self.additional_details).chars(
            50, truncate="..."
        )
        return f"{self.product.name}: {truncated_description}"

    class Meta:
        verbose_name = _("Additional Information")
        verbose_name_plural = _("Additional Informations")


class Review(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("user"),
        related_name="reviews",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_("product"),
        related_name="reviews",
    )
    text = models.CharField(_("text"), max_length=120)
    is_valid = models.BooleanField(_("is valid"), default=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)

    def __str__(self):
        truncated_message = Truncator(self.text).chars(50, truncate="...")
        return f"{self.user.phone} wrote '{truncated_message}' for {self.product.name} product"

    class Meta:
        ordering = ("-created_at",)
        verbose_name = _("Review")
        verbose_name_plural = _("Reviews")
