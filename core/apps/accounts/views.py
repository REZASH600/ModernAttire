from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import FormView, UpdateView

from . import forms

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
