# yourapp/forms.py
from dal import autocomplete
from django import forms
from app.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'user': autocomplete.ModelSelect2(url='app:owner-autocomplete')
        }
