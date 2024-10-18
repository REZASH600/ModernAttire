from django.shortcuts import render, get_object_or_404, reverse
from django.views.generic import TemplateView, ListView
from django.views import View

from . import models, modules
from django.db.models import Count
from django.http import JsonResponse, Http404


class HomeView(TemplateView):
    template_name = "products/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["offers"] = [
            offer
            for offer in models.Offer.objects.filter(is_publish=True)
            if offer.is_active
        ][:4]

        context["featured_products"] = models.Product.objects.annotate(
            like_count=Count("likes")
        ).order_by("-like_count")[:12]

        context["recent_products"] = models.Product.objects.filter(is_publish=True)[:12]
        context["brands"] = models.Brand.objects.filter(is_publish=True)[:12]

        return context


class LikeView(View):

    def get(self, request, product_id):
        product = get_object_or_404(models.Product, id=product_id)

        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            if not self.request.user.is_authenticated:
                return JsonResponse(
                    {
                        "url": f"{reverse('accounts:login')}?next={request.GET.get('current_url')}"
                    }
                )

            if product.likes.filter(id=self.request.user.id).exists():
                product.likes.remove(self.request.user)
                is_liked = False
            else:
                product.likes.add(self.request.user)
                is_liked = True

            number_like = self.request.user.liked_products.all().count()
            return JsonResponse(
                {"isLiked": is_liked, "numberLike": number_like}, status=200
            )

        raise Http404()


class ProductListView(ListView):
    paginate_by = 5



    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        paginator = self.get_paginator(queryset, self.get_paginate_by(queryset))
        page_number = request.GET.get("page") or 1
        page_obj = paginator.get_page(page_number)

        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            saved_list = []
            is_authenticated = self.request.user.is_authenticated
            for product in page_obj.object_list:

                offer = product.offer if product.offer.is_active else None

                is_liked = product.likes.filter(
                    id=self.request.user.id if is_authenticated else None
                ).exists()

                product_json = {
                    "imageUrl": product.images.all().first().image_file.url,
                    "redirectUrl": reverse("products:list"), # change to product detail
                    "name": product.name,
                    "price": product.price,
                    "bestDiscountedPrice": offer.apply_discount(product) if offer else product.price ,
                    "isLiked": is_liked,
                    "urlLike": reverse(
                        "products:like", kwargs={"product_id": product.id}
                    ),
                }

                saved_list.append(product_json)

            pagination_data = {
                "has_other_pages": page_obj.has_other_pages(),
                "has_previous": page_obj.has_previous(),
                "has_next": page_obj.has_next(),
                "num_pages": page_obj.paginator.num_pages,
                "current_page": page_obj.number,
                "previous_page_number": (
                    page_obj.previous_page_number() if page_obj.has_previous() else None
                ),
                "next_page_number": (
                    page_obj.next_page_number() if page_obj.has_next() else None
                ),
            }
            return JsonResponse(
                {"products": saved_list, "pagination": pagination_data}, safe=False
            )

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        colors = models.Color.objects.all()
        sizes = models.Size.objects.all()

        selected_colors = self.request.GET.getlist("color")
        selected_sizes = self.request.GET.getlist("size")

        context["colors"] = colors
        context["sizes"] = sizes
        context["selected_colors"] = selected_colors
        context["selected_sizes"] = selected_sizes

        return context

    def get_queryset(self):
        queryset = modules.ProductFilter(self.request.GET)
        return queryset.qs

    def get_paginate_by(self, queryset):
        per_page = self.request.GET.get("per_page", self.paginate_by)
        return int(per_page)
