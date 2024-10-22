from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import FormView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.orders.models import City
from . import forms


class CheckoutView(LoginRequiredMixin, FormView):
    template_name = "orders/checkout.html"
    form_class = forms.AddressForm
    success_url = reverse_lazy("order:checkout")

    def get_form_kwargs(self):

        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request 
        return kwargs

    def form_valid(self, form):
        address = form.save(commit=False)
        address.user = self.request.user
        address.save()
        next_page = self.request.GET.get("next",self.success_url)
        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"url": next_page})
        return super().form_valid(form)


class LoadCitesView(View):
    def get(self, request):
        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            province_id = request.GET.get("province_id")
            cities = City.objects.filter(province_id=province_id).values("id", "name")
            return JsonResponse(list(cities), safe=False)
        return redirect("order:checkout")
