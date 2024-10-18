from rest_framework.routers import DefaultRouter
from . import views


app_name = "api-v1"

router = DefaultRouter()
router.register(r"province", views.ProvinceView, basename="province")
router.register(r"city", views.CityView, basename="city")
router.register(r"address", views.AddressView, basename="address")
router.register(r"order", views.OrderView, basename="order")
router.register(r"order_item", views.OrderItemView, basename="order_item")


urlpatterns = router.urls
