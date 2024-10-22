from django.urls import path, include
from . import views

app_name = "order"
urlpatterns = [
    path("api/v1/", include("apps.orders.api.v1.urls")),
    path("checkout/", views.CheckoutView.as_view(), name="checkout"),
    path("get/cities/", views.LoadCitesView.as_view(), name="get_cities"),
]
