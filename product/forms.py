from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'product_category', 'description','access_range']

class ProductFullForm(ProductForm): #extending form
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta(ProductForm.Meta):
        fields = ProductForm.Meta.fields + ['image',]