from django.urls import path
from . import views

app_name = "cart"
urlpatterns = [
    path("list/", views.CartView.as_view(), name="cart_list"),
    path(
        "product/remove/<str:unique_name>/",
        views.RemoveProductView.as_view(),
        name="remove_product",
    ),
    path(
        "product/update/quantity/<str:unique_name>/<str:value>/",
        views.UpdateQuantityView.as_view(),
        name="update_quantity",
    ),
]