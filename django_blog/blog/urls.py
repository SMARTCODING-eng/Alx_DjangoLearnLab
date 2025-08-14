from django.urls import path
from . import views


urlpatterns = [
    path('/post/', views.ListView.as_view(), name='post-list'),
    path('post/<int:pk>/', views.DetailView.as_view(), name='post-detail'),
    path('post/new/', views.CreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', views.UpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', views.DeleteView.as_view(), name='post-delete'),
    path('tags/<slug:tag_slug>/', views.PostByTagListView.as_view(), name='posts-by-tag'),
    path('search/', views.search_view, name='search'),

    # Comments URLs
    path('post/<int:pk>/comments/new/', views.CommentCreateView.as_view(), name='post-comment-create'),
    path('post/comment/<int:pk>/update/', views.CommentUpdateView.as_view(), name='post-comment-update'),
    path('post/comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='post-comment-delete'),

    # Authentication and registration URLs
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
]
