from django.shortcuts import render, get_object_or_404, reverse, redirect
from apps.products.models import Product
from .cart import CartSession
from django.http import JsonResponse
from django.views import View

class CartView(View):

    def get(self, request):
        cart = CartSession(self.request)
        return render(request, "cart/cart.html", {"cart": cart})

    def post(self, request):
        size = request.POST.get("size")
        color = request.POST.get("color")
        quantity = request.POST.get("quantity")
        product_slug = request.POST.get("slug")
        product = get_object_or_404(Product, slug=product_slug)
        cart = CartSession(self.request)
        cart.add_product(product, size, color, quantity)
        return JsonResponse({"url": reverse("cart:cart_list")}, status=200)


class RemoveProductView(View):
    def get(self, request, unique_name):
        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            cart = CartSession(self.request)
            cart.remove_product(unique_name)
            return JsonResponse(
                {"totalCart": cart.get_total_price_of_cart()}, status=200
            )
        return redirect("cart:cart_list")


class UpdateQuantityView(View):

    def get(self, request, unique_name, value):
        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            cart = CartSession(self.request)
            cart.update_product_quantity(unique_name, value)
            return JsonResponse(
                {
                    "totalCart": f"{cart.get_total_price_of_cart():,.2f}",
                    "totalPrice": f"${cart.get_total_price_of_product(unique_name):,.2f}",
                },
                status=200,
            )
        return redirect("cart:cart_list")
