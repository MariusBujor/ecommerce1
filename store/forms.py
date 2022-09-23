from django import forms
from .models import ReviewRating, Product


class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['subject', 'review', 'rating']


class AddProduct(forms.ModelForm):
    
    class Meta:
        model = Product
        exclude = ('created_by',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
