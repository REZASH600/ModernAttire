from django.urls import path, include
from . import views

app_name = "accounts"

urlpatterns = [
    path("api/v1/", include("apps.accounts.api.v1.urls")),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("login/", views.LoginView.as_view(), name="login"),
]
