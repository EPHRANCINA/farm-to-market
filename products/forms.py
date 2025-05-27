from django import forms
from .models import Product

class ProductImageForm(forms.Form):
    images = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        required=False,
        help_text='You can upload multiple images'
    )

class ProductForm(forms.ModelForm):
    # Seller Information Fields
    seller_name = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your full name'}),
        help_text='Your full name as it will appear to buyers'
    )
    
    seller_email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email address'}),
        help_text='Your email address for buyers to contact you'
    )
    
    seller_phone = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}),
        help_text='Your phone number for buyers to contact you'
    )
    
    seller_address = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your address'}),
        help_text='Your address where buyers can find you'
    )

    # Product Information Fields
    harvest_date = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        help_text='When was this product harvested?'
    )
    
    farm_location = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter farm location'}),
        help_text='Location of your farm'
    )
    
    growing_method = forms.ChoiceField(
        choices=[
            ('organic', 'Organic'),
            ('conventional', 'Conventional'),
            ('hydroponic', 'Hydroponic'),
            ('greenhouse', 'Greenhouse'),
        ],
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'quantity', 'category', 
                 'harvest_date', 'farm_location', 'growing_method', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter product name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe your product'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Enter price per unit'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'placeholder': 'Enter available quantity'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        product = super().save(commit=False)
        if commit:
            product.save()
        return product 