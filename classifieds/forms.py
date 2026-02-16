from django import forms
from django.forms.models import inlineformset_factory, BaseInlineFormSet
from taggit.models import Tag

from .models import Ad, Subcategory, City, AdImage


class AdAddForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Additional options',
        help_text='You can select one or more options that apply to your ad.',
    )

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
            'tags',
        )

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control', 'id': 'id_category'}),
            'subcategory': forms.Select(attrs={'class': 'form-control', 'id': 'id_subcategory'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'region': forms.Select(attrs={'class': 'form-control', 'id': 'id_region'}),
            'city': forms.Select(attrs={'class': 'form-control', 'id': 'id_city'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['subcategory'].queryset = Subcategory.objects.none()
        self.fields['city'].queryset = City.objects.none()


class AdImageForm(forms.ModelForm):
    class Meta:
        model = AdImage
        fields = ('image',)


AdImageFormSet = inlineformset_factory(
    Ad,
    AdImage,
    form=AdImageForm,
    extra=7,
    max_num=7,
    validate_max=True,
    can_delete=False,
)
