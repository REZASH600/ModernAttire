from django import template
from apps.products import models
from django.shortcuts import get_object_or_404

register = template.Library()


@register.simple_tag
def product_offer(product):
    offer = product.offer
    if offer and offer.is_active:
        return offer.apply_discount(product)
    return None


@register.simple_tag(takes_context=True)
def is_like(context, product_id):
    request = context["request"]
    user = request.user
    try:
        product = models.Product.objects.get(id=product_id)

    except models.Product.DoesNotExist:
        return False

    if user.is_authenticated:
        return product.likes.filter(id=user.id).exists()


    return False


@register.simple_tag
def update_url_param(value, field_name, urlencode=None):
    url = "?{}={}".format(field_name, value)

    if urlencode is not None:
        querystring = urlencode.split("&")
        queryfilter = filter(lambda p: p.split("=")[0] != field_name, querystring)
        query = "&".join(queryfilter)
        url = "{}&{}".format(url, query)

    return url
