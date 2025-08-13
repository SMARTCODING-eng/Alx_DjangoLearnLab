from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomUserAuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin



def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('blog-home')      
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', {'form': form})


@login_required
def profile_view(request):
    return render(request, 'blog/profile.html', {'user': request.user})


def login_view(request):
    if request.method == 'POST':
        form = CustomUserAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('blog-home')
    else:
        form = CustomUserAuthenticationForm()
    return render(request, 'blog/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('blog-home')

class ListView(ListView):
    """View to list all blog posts"""
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'


class DetailView(DetailView):
    """View to display a single blog post"""
    model = Post
    template_name = 'blog/post_detail.html'


class CreateView(LoginRequiredMixin, CreateView):
    """View to allow authenticated users to create new posts"""
    model = Post
    template_name = 'blog/post_create.html'
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    


class UpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """View to allow authenticated users to update their posts"""
    model = Post
    template_name = 'blog/post_edit.html'
    fields = ['title', 'content']

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class DeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """View to allow authenticated user to delete their posts"""
    model = Post
    template_name = 'blog/post_delete.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
