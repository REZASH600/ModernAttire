from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from apps.accounts.validations import validate_phone
from apps.products.models import Product
User = get_user_model()


class Province(models.Model):
    name = models.CharField(_("name"), max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Province")
        verbose_name_plural = _("provinces")


class City(models.Model):
    name = models.CharField(_("name"), max_length=100)
    province = models.ForeignKey(
        Province,
        related_name="cities",
        on_delete=models.CASCADE,
        verbose_name=_("province"),
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("City")
        verbose_name_plural = _("City")


class Address(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=_("user"), related_name="addresses"
    )
    recipient_name = models.CharField(_("recipient name"), max_length=255)
    recipient_phone_number = models.CharField(
        max_length=11, validators=[validate_phone]
    )
    street = models.CharField(_("street name"), max_length=255)
    postal_code = models.CharField(_("postal code"), max_length=20)
    building_number = models.CharField(_("building number"), max_length=10)
    unit = models.CharField(_("unit"), max_length=10, blank=True, null=True)
    is_active = models.BooleanField(_("is active"), default=True)

    province = models.ForeignKey(
        Province,
        on_delete=models.CASCADE,
        verbose_name=_("province"),
        related_name="addresses",
    )

    city = models.ForeignKey(
        City, on_delete=models.CASCADE, verbose_name=_("city"), related_name="addresses"
    )

    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    def __str__(self):
        address = f"{self.recipient_name}, {self.building_number} {self.street}"
        
        if self.unit:
            address += f", Unit {self.unit}"

        address += f", {self.city.name}, {self.province.name}, {self.postal_code}"
        
        return address

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")


class Order(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=_("user"), related_name="orders"
    )
    address = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("address"),
        related_name="orders",
    )
    total_price = models.DecimalField(_("total price"), max_digits=15, decimal_places=2)
    is_paid = models.BooleanField(_("is paid"), default=False)
    is_discount = models.BooleanField(_("is discount"), default=False)

    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    def formatted_price(self):
        return f"{self.total_price:,.2f}"

    def __str__(self):
        return f"Order #{self.id} by {self.user}"

    class Meta:
        ordering = ("-updated_at", "-created_at")
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, verbose_name=_("order"), related_name="items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_("product"),
        related_name="order_items",
        
    )

    size = models.CharField(_("size"), max_length=30)
    color = models.CharField(_("color"), max_length=30)
    quantity = models.PositiveSmallIntegerField(_("quantity"), default=1)
    final_price = models.DecimalField(_("final price"), max_digits=12, decimal_places=2)

    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    def __str__(self):
        return f"{self.product.name} ({self.size}/{self.color}) x {self.quantity}"

    class Meta:
        ordering = ("-updated_at", "-created_at")
        verbose_name = _("Order Item")
        verbose_name_plural = _("Order Items")
