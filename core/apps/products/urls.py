from django.urls import path, include
from . import views

app_name = "products"

urlpatterns = [
    path("api/v1/", include("apps.products.api.v1.urls")),
    path("like/<int:product_id>/", views.LikeView.as_view(), name="like"),
]
