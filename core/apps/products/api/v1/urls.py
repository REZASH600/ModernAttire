from rest_framework.routers import DefaultRouter

from . import views

app_name = "api-v1"

router = DefaultRouter()
router.register(r"size", views.SizeViewSet, basename="size")
router.register(r"color", views.ColorViewSet, basename="color")
router.register(r"category", views.CategoryViewSet, basename="category")
router.register(r"brand", views.BrandViewSet, basename="brand")
router.register(r"offer", views.OfferViewSet, basename="offer")
router.register(r"product", views.ProductViewSet, basename="product")
router.register(r"image", views.ImageViewSet, basename="image")
router.register(r"extra_info", views.AdditionalInformationViewSet, basename="extra_info")
router.register(r"review", views.ReviewViewSet, basename="review")
urlpatterns = router.urls
