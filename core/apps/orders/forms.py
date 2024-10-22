from django import forms


from django import forms
from .models import Address, City, Province


class AddressForm(forms.ModelForm):
    user = forms.IntegerField(required=False)

    class Meta:
        model = Address
        fields = [
            "user",
            "recipient_name",
            "recipient_phone_number",
            "building_number",
            "unit",
            "street",
            "postal_code",
            "city",
            "province",
        ]
        widgets = {
            "city": forms.Select(),
            "province": forms.Select(),
            "recipient_name": forms.TextInput({"placeholder": "John Doe"}),
            "recipient_phone_number": forms.TextInput(),
            "building_number": forms.TextInput({"placeholder": "123"}),
            "unit": forms.TextInput({"placeholder": "4B"}),
            "street": forms.TextInput({"placeholder": "Main St"}),
            "postal_code": forms.TextInput({"placeholder": "12345"}),
        }

    def __init__(self, request,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["city"].queryset = City.objects.all()
        self.fields["province"].queryset = Province.objects.all()

        if request.user.is_authenticated:
            self.initial["recipient_phone_number"] = request.user.phone

        if self.fields["city"].queryset.exists():
            self.initial["city"] = self.fields["city"].queryset.first().id
        if self.fields["province"].queryset.exists():
            self.initial["province"] = self.fields["province"].queryset.first().id
