from apps.products import models


def categories(request):
    return {"categories": models.Category.objects.filter(is_publish=True)}
