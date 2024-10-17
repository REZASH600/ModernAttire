from django.shortcuts import render
from . import forms
from django.urls import reverse_lazy
from . import tasks
from django.views.generic import FormView


class ContactUsView(FormView):
    template_name = "contact/contact.html"
    form_class = forms.ContactForm
    success_url = reverse_lazy("contact:contact_us")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        cd = form.cleaned_data
        tasks.send_contact_email.apply_async(args=[cd["subject"], cd["message"], cd["email"]])
        return super().form_valid(form)
