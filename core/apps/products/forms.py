from django import forms
from . import models


class ReviewForm(forms.ModelForm):
    user = forms.IntegerField(required=False)
    product = forms.IntegerField(required=False)

    class Meta:
        model = models.Review
        fields = ["user", "product", "text"]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        self.product = kwargs.pop("product", None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):

        obj = super().save(commit=False)

        if commit:

            if self.request and self.request.user.is_authenticated:

                obj.user = self.request.user

            if self.product:
                obj.product = self.product

            obj.save()

        return obj
