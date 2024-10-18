from django.contrib import admin
from . import models


@admin.register(models.Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ["recipient_name", "recipient_phone_number", "is_active"]
    list_filter = ["province", "city", "is_active"]
    list_editable = ["is_active"]
    search_fields = ["user__phone","user__username","recipient_name", "recipient_phone_number"]


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["user", "formatted_price", "is_paid", "is_discount"]
    list_filter = ["is_paid", "is_discount"]
    list_editable = ["is_paid", "is_discount"]
    search_fields = ["user__phone","user__username"]


@admin.register(models.OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["order", "product", "size", "color", "quantity", "final_price"]
    list_filter = ["product", "size", "color"]
    search_fields = ["product__name", "order__user__phone"]


admin.site.register(models.Province)
admin.site.register(models.City)
