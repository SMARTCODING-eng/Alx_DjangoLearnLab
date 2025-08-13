from django.urls import path
from . import views

urlpatterns = [
    path('/posts/', views.ListView.as_view(), name='post-list'),
    path('posts/<int:pk>/', views.DetailView.as_view(), name='post-detail'),
    path('posts/new/', views.CreateView.as_view(), name='post-create'),
    path('posts/<int:pk>/edit/', views.UpdateView.as_view(), name='post-edit'),
    path('posts/<int:pk>/delete/', views.DeleteView.as_view(), name='post-delete'),
    # Authentication and registration URLS
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
]