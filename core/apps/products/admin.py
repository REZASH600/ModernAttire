from django.contrib import admin
from . import models
from django.utils.translation import gettext_lazy as _

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "is_publish"]
    list_editable = ["is_publish"]
    list_filter = ["is_publish"]
    search_fields = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(models.Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ["name", "is_publish", "show_image"]
    list_editable = ["is_publish"]
    list_filter = ["is_publish"]
    search_fields = ("name",)


@admin.register(models.Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ["title", "discount_percentage", "is_publish"]
    list_editable = ["discount_percentage", "is_publish"]
    list_filter = ["is_publish"]
    search_fields = ["title"]


class ImageProductInline(admin.TabularInline):
    model = models.Image
    extra = 0
    readonly_fields = ["show_image"]


class GenderFilterList(admin.SimpleListFilter):
    title = _("Gender")
    parameter_name = "gender"

    def lookups(self, request, model_admin):
        return (("M", _("Male")), ("F", _("Female")))

    def queryset(self, request, queryset):
        if self.value():
            return models.Product.objects.filter(gender=self.value())

        return models.Product.objects.all()


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "formatted_price", "quantity", "is_publish"]
    list_editable = ["quantity", "is_publish"]
    list_filter = ["is_publish", GenderFilterList]
    search_fields = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ImageProductInline]


@admin.register(models.Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ["__str__", "show_image"]
    search_fields = ["product__name"]


@admin.register(models.AdditionalInformation)
class AdditionalInformationAdmin(admin.ModelAdmin):
    search_fields = ["product__name"]   


@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["__str__", "is_valid"]
    list_editable = ["is_valid"]
    list_filter = ["is_valid"]
    search_fields = ["product__name", "product__slug", "user__phone", "user__email"]

admin.site.register(models.Size)
admin.site.register(models.Color)
