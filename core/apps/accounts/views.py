from django.shortcuts import redirect
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from . import forms
from django.contrib import messages
from django.urls import reverse_lazy

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
