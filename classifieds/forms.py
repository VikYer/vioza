from django import forms
from .models import Ad, Subcategory, City


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
           'category': forms.Select(attrs={'class': 'form-control', 'id': 'id_category'}),
           'subcategory': forms.Select(attrs={'class': 'form-control', 'id': 'id_subcategory'}),
           'price': forms.NumberInput(attrs={'class': 'form-control'}),
           'region': forms.Select(attrs={'class': 'form-control', 'id': 'region'}),
           'city':  forms.Select(attrs={'class': 'form-control', 'id': 'city'}),
           'description': forms.Textarea(attrs={'class': 'form-control'}),
           'status': forms.Select(attrs={'class': 'form-control'})
       }

   def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['subcategory'].queryset = Subcategory.objects.none()
        self.fields['city'].queryset = City.objects.none()
