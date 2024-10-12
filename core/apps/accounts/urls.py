from django.urls import include, path

from . import views

app_name = "accounts"

urlpatterns = [
    path("api/v1/", include("apps.accounts.api.v1.urls")),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("register/verify/otp/<int:user_id>/", views.VerifyRegistrationOtp.as_view(), name="verify_register_otp"),
    path("password/forgot/", views.ForgotPasswordView.as_view(), name="forgot_password"),
    path("password/verify/otp/<int:user_id>/", views.VerifyForgotPasswordOtp.as_view(), name="verify_forgot_password_otp"),
    path("password/reset/<str:token>/", views.ResetPasswordView.as_view(), name="reset_password"),

]
