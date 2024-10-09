from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy,reverse
from django.views import View
from django.views.generic.edit import FormView, UpdateView
from . import models
from . import forms
from . import tasks

User = get_user_model()


class ProfileView(LoginRequiredMixin, UpdateView):

    queryset = User.objects.filter(is_active=True)
    form_class = forms.ProfileForm
    template_name = "accounts/profile.html"
    success_url = reverse_lazy("accounts:profile")

    def get_object(self):
        return self.request.user

    def form_valid(self, form):

        form.save(request=self.request)
        messages.success(self.request, "Profile updated successfully!")

        return redirect(self.success_url)


class LoginView(FormView):
    template_name = "accounts/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("accounts:profile")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("/")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        cd = form.cleaned_data
        user = authenticate(username=cd["identifier"], password=cd["password"])
        if user is None:
            form.add_error(None, "Invalid username or password.")
            return self.form_invalid(form)

        login(self.request, user)
        next_page = self.request.GET.get("next")
        return redirect(next_page) if next_page else super().form_valid(form)


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect("/")


class RegisterView(View):

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("/")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = forms.RegisterForm()
        return render(request, "accounts/register.html", {"form": form})

    def post(self, request):
        form = forms.RegisterForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(
                phone=cd["phone"], username=cd["username"], password=cd["new_password"]
            )
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            return redirect("accounts:verify_register_otp", user_id=user.id)
        return render(request, "accounts/register.html", {"form": form})


class VerifyRegistrationOtp(LoginRequiredMixin, View):

    def dispatch(self, request, user_id, *args, **kwargs):
        next_page = self.request.GET.get("next", "/")
        user = self.request.user
        if user.id != user_id or user.is_verify:
            return redirect(next_page)
        return super().dispatch(request, user_id, *args, **kwargs)

    def get(self, request, user_id):
        form = forms.CheckOtpForm()
        otp = models.Otp.get_active_otp(user_id=user_id)
        user = self.request.user
        if otp is None:
            otp = models.Otp.create_otp_for_user(user_id)
            tasks.send_otp_sms.apply_async(
                args=[user.username, user.phone, otp.code]
            )
            
        return render(request, "accounts/check-otp.html", {"form": form})

    def post(self, request, user_id):
        form = forms.CheckOtpForm(request.POST)
        next_page = request.POST.get("next", reverse("accounts:profile"))

        if form.is_valid():
            otp = models.Otp.get_active_otp(user_id, form.cleaned_data["code"])
            if otp:
                user = User.objects.get(id=user_id)
                user.is_verify = True
                user.save()
                otp.delete()
                return redirect(next_page)

            form.add_error("code", "The OTP has expired. Please request a new one.")

        return render(request, "accounts/check-otp.html", {"form": form})
