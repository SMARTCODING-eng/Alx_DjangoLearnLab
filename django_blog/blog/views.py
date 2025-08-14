from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import CustomUserCreationForm, CustomUserAuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post, Comment


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

    def get_queryset(self):
        return Post.objects.all().order_by('-publeished_date')


class DetailView(DetailView):
    """View to display a single blog post"""
    model = Post
    template_name = 'blog/post_detail.html'

    def get_queryset(self):
        return Post.objects.filter(id=self.kwargs['pk'])


class CreateView(LoginRequiredMixin, CreateView):
    """View to allow authenticated users to create new posts"""
    model = Post
    form_class =PostForm
    template_name = 'blog/post_create.html'
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    


class UpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """View to allow authenticated users to update their posts"""
    model = Post
    form_class = PostForm
    template_name = 'blog/post_edit.html'

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


class CommentListView(LoginRequiredMixin, ListView):
    """View to list all comments on a post"""
    model = Comment
    template_name = 'blog/post_detail.html'
    context_object_name = 'comments'

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['post_id'])
    

class CommentCreateView(CreateView, LoginRequiredMixin):
    """View to allow authenticated users to create comments on a post"""
    model = Comment
    template_name = 'blog/comment_form.html'
    fields = ['content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        form.instance.post = post
        return super().form_valid(form)


class CommentUpdateView(UpdateView, LoginRequiredMixin, UserPassesTestMixin):
    model = Comment
    template_name = 'blog/comment_form.html'
    fields = ['content']

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author


class CommentDeleteView(DeleteView, LoginRequiredMixin, UserPassesTestMixin):
    """View to delete comment made by a particular author"""
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author
    
    def get_success_url(self):
        return self.object.post.get_absolute_url()
