from django import forms
from .models import Ad


class AdAddForm(forms.ModelForm):
   class Meta:
       model = Ad
       fields = (
           'title',
           'category',
           'subcategory',
           'price',
           'region',
           'city',
           'description',
           'status',
       )

       widgets = {
           'title': forms.TextInput(attrs={'class': 'form-control'}),
           'category': forms.Select(attrs={'class': 'form-control'}),
           'subcategory': forms.Select(attrs={'class': 'form-control'}),
           'price': forms.NumberInput(attrs={'class': 'form-control'}),
           'region': forms.Select(attrs={'class': 'form-control'}),
           'city':  forms.Select(attrs={'class': 'form-control'}),
           'description': forms.Textarea(attrs={'class': 'form-control'}),
           'status': forms.Select(attrs={'class': 'form-control'}),
       }