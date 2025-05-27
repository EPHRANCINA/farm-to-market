from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator, EmailValidator
from django.core.exceptions import ValidationError
from .models import User

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        validators=[EmailValidator(message="Please enter a valid email address")],
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z\s]*$',
                message='First name should only contain letters and spaces'
            )
        ],
        widget=forms.TextInput(attrs={'class': 'form-control', 'size': 30})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z\s]*$',
                message='Last name should only contain letters and spaces'
            )
        ],
        widget=forms.TextInput(attrs={'class': 'form-control', 'size': 30})
    )
    phone_number = forms.CharField(
        max_length=10,
        required=True,
        validators=[
            RegexValidator(
                regex=r'^(06|07)\d{8}$',
                message='Phone number must start with 06 or 07 and be 10 digits long'
            )
        ],
        help_text='Enter a 10-digit number starting with 06 or 07',
        widget=forms.TextInput(attrs={'class': 'form-control', 'size': 30, 'pattern': '^(06|07)\d{8}$'})
    )
    address = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'size': 30})
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text='Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one number, and one special character.'
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'address', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'size': 30}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('This username is already taken')
        if len(username) < 4:
            raise ValidationError('Username must be at least 4 characters long')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('This email is already registered')
        return email

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if not phone.startswith(('06', '07')):
            raise ValidationError('Phone number must start with 06 or 07')
        if len(phone) != 10:
            raise ValidationError('Phone number must be 10 digits long')
        if User.objects.filter(phone_number=phone).exists():
            raise ValidationError('This phone number is already registered')
        return phone

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 8:
            raise ValidationError('Password must be at least 8 characters long')
        if not any(char.isupper() for char in password):
            raise ValidationError('Password must contain at least one uppercase letter')
        if not any(char.islower() for char in password):
            raise ValidationError('Password must contain at least one lowercase letter')
        if not any(char.isdigit() for char in password):
            raise ValidationError('Password must contain at least one number')
        if not any(char in '!@#$%^&*()_+-=[]{}|;:,.<>?/~`' for char in password):
            raise ValidationError('Password must contain at least one special character')
        return password

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise ValidationError('Passwords do not match')
        
        return cleaned_data

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(
        required=True,
        validators=[EmailValidator(message="Please enter a valid email address")],
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z\s]*$',
                message='First name should only contain letters and spaces'
            )
        ],
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z\s]*$',
                message='Last name should only contain letters and spaces'
            )
        ],
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    phone_number = forms.CharField(
        max_length=10,
        required=True,
        validators=[
            RegexValidator(
                regex=r'^(06|07)\d{8}$',
                message='Phone number must start with 06 or 07 and be 10 digits long'
            )
        ],
        help_text='Enter a 10-digit number starting with 06 or 07',
        widget=forms.TextInput(attrs={'class': 'form-control', 'pattern': '^(06|07)\d{8}$'})
    )
    address = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'address']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise ValidationError('This email is already registered')
        return email

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if not phone.startswith(('06', '07')):
            raise ValidationError('Phone number must start with 06 or 07')
        if len(phone) != 10:
            raise ValidationError('Phone number must be 10 digits long')
        if User.objects.exclude(pk=self.instance.pk).filter(phone_number=phone).exists():
            raise ValidationError('This phone number is already registered')
        return phone 