from django import forms
from .models import CustomOrder

class CustomOrderRequestForm(forms.ModelForm):
    class Meta:
        model = CustomOrder
        fields = ['category', 'size', 'colors', 'message', 'reference_image']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),
        }

class ArtisanStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomOrder
        fields = ['status', 'customization_price']
