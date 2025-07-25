from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.html import escape
from .models import Book, Author
from datetime import datetime

class SecureForm(forms.Form):
    """
    Base form with security enhancements
    """
    def clean(self):
        cleaned_data = super().clean()
        # Escape all string fields to prevent XSS
        for field_name, value in cleaned_data.items():
            if isinstance(value, str):
                cleaned_data[field_name] = escape(value)
        return cleaned_data


class UserRegistrationForm(UserCreationForm, SecureForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'autocomplete': 'email'
        })
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'autocomplete': 'username'
        })
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email').lower().strip()
        if User.objects.filter(email=email).exists():
            raise ValidationError('This email is already registered.')
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username').strip()
        if len(username) < 4:
            raise ValidationError('Username must be at least 4 characters long.')
        return username


class BookForm(forms.ModelForm, SecureForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '200'
            }),
            'author': forms.Select(attrs={
                'class': 'form-control'
            }),
            'publication_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1900',
                'max': '2100'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author'].queryset = Author.objects.all().order_by('name')
        self.fields['author'].empty_label = "Select an author"

    def clean_title(self):
        title = self.cleaned_data.get('title').strip()
        if len(title) < 2:
            raise ValidationError('Title must be at least 2 characters long.')
        return title

    def clean_publication_year(self):
        year = self.cleaned_data.get('publication_year')
        current_year = datetime.now().year
        if year < 1900 or year > current_year + 2:
            raise ValidationError(
                f'Publication year must be between 1900 and {current_year + 2}'
            )
        return year


class ExampleForm(SecureForm):
    """
    Example form demonstrating security best practices
    """
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your name'
        })
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3
        }),
        required=False
    )

    def clean_name(self):
        name = self.cleaned_data.get('name').strip()
        if not name.isprintable():
            raise ValidationError('Name contains invalid characters.')
        return name


class CustomAuthenticationForm(AuthenticationForm, SecureForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'autocomplete': 'username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'autocomplete': 'current-password'
        })
    )