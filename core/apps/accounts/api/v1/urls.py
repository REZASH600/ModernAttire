from rest_framework.routers import DefaultRouter
from . import views


app_name = "api-v1"

router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')
urlpatterns = router.urls