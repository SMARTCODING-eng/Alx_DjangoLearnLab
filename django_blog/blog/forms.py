from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Post
 


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email',)


class CustomUserAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'password')

class PostForm(forms.ModelForm):
    """Form for creating and Updating new post and automatically set author based on logged-in user"""
    class Meta:
        model = Post
        fields = ['title', 'content']

    def save(self, commit=True):
        post = self.instance()
        if commit:
            post.save()
        return post