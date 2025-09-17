from django.forms import ModelForm
from main.models import Product2

class Product2Form(ModelForm):
    class Meta:
        model = Product2
        fields = [
            "name",
            "price",
            "description",
            "thumbnail",
            "category",
            "is_featured",
        ]
