from django.shortcuts import render, get_object_or_404, reverse
from django.views.generic import TemplateView
from django.views import View

from . import models
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
