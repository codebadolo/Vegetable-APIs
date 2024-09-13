from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter product name', 'style': 'width: 50%;'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'style': 'width: 50%;'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 25%;'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 25%;'}),
            'category': forms.Select(attrs={'class': 'form-control', 'style': 'width: 50%;'}),
        }
