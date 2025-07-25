from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Book, Author


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)


    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered.')
        return email
    

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author'].queryset = Author.objects.all().order_by('name')
