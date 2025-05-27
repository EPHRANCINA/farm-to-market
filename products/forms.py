from django import forms
from django.core.validators import RegexValidator, EmailValidator, MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from .models import Product
from django.utils import timezone

class ProductImageForm(forms.Form):
    images = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        required=False,
        help_text='You can upload multiple images'
    )

    def clean_images(self):
        images = self.cleaned_data.get('images')
        if images:
            if images.size > 5 * 1024 * 1024:  # 5MB limit
                raise ValidationError('Image size must be less than 5MB')
            if not images.content_type.startswith('image/'):
                raise ValidationError('File must be an image')
        return images

class ProductForm(forms.ModelForm):
    # Seller Information Fields
    seller_name = forms.CharField(
        max_length=200,
        required=True,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z\s]*$',
                message='Name should only contain letters and spaces'
            )
        ],
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your full name'}),
        help_text='Your full name as it will appear to buyers'
    )
    
    seller_email = forms.EmailField(
        required=True,
        validators=[EmailValidator(message="Please enter a valid email address")],
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email address'}),
        help_text='Your email address for buyers to contact you'
    )
    
    seller_phone = forms.CharField(
        max_length=10,
        required=True,
        validators=[
            RegexValidator(
                regex=r'^(06|07)\d{8}$',
                message='Phone number must start with 06 or 07 and be 10 digits long'
            )
        ],
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number', 'pattern': '^(06|07)\d{8}$'}),
        help_text='Enter a 10-digit number starting with 06 or 07'
    )
    
    seller_address = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your address'}),
        help_text='Your address where buyers can find you'
    )

    # Product Information Fields
    name = forms.CharField(
        max_length=200,
        required=True,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9\s\-_]+$',
                message='Product name can only contain letters, numbers, spaces, hyphens, and underscores'
            )
        ],
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter product name'})
    )

    description = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe your product'})
    )

    price = forms.DecimalField(
        required=True,
        validators=[
            MinValueValidator(0.01, message='Price must be greater than 0'),
            MaxValueValidator(1000000, message='Price cannot exceed 1,000,000')
        ],
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Enter price per unit'})
    )

    quantity = forms.IntegerField(
        required=True,
        validators=[
            MinValueValidator(1, message='Quantity must be at least 1'),
            MaxValueValidator(10000, message='Quantity cannot exceed 10,000')
        ],
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'placeholder': 'Enter available quantity'})
    )

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

    image = forms.ImageField(
        required=True,
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        help_text='Upload a clear image of your product'
    )
    
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'quantity', 'category', 
                 'harvest_date', 'farm_location', 'growing_method', 'image']

    def clean_seller_phone(self):
        phone = self.cleaned_data.get('seller_phone')
        if not phone.startswith(('06', '07')):
            raise ValidationError('Phone number must start with 06 or 07')
        if len(phone) != 10:
            raise ValidationError('Phone number must be 10 digits long')
        return phone

    def clean_seller_name(self):
        name = self.cleaned_data.get('seller_name')
        if len(name.split()) < 2:
            raise ValidationError('Please enter your full name (first and last name)')
        return name

    def clean_harvest_date(self):
        harvest_date = self.cleaned_data.get('harvest_date')
        if harvest_date > timezone.now().date():
            raise ValidationError('Harvest date cannot be in the future')
        return harvest_date

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 5 * 1024 * 1024:  # 5MB limit
                raise ValidationError('Image size must be less than 5MB')
            if not image.content_type.startswith('image/'):
                raise ValidationError('File must be an image')
        return image

    def clean(self):
        cleaned_data = super().clean()
        price = cleaned_data.get('price')
        quantity = cleaned_data.get('quantity')
        
        if price and quantity:
            total_value = price * quantity
            if total_value > 1000000:  # 1 million limit
                raise ValidationError('Total value of the product cannot exceed 1,000,000')
        
        return cleaned_data

    def save(self, commit=True):
        product = super().save(commit=False)
        if commit:
            product.save()
        return product 