from django.urls import path
from .views import list_books
from .views import LibraryDetailView
from . import views 
from django.contrib.auth import views as auth_views


app_name = 'relationship_app'

urlpatterns = [
    path('books/', list_books, name='book_list'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),

    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),

    path('admin_dashboard/', views.admin_view, name='admin_dashboard'),
    path('librarian_dashboard/', views.librarian_view, name='librarian_dashboard'),
    path('member_dashboard/', views.member_view, name='member'),

    path('books/add/', views.add_book, name='add_book/'),
    path('books/<int:pk>/edit/', views.edit_book, name='edit_book/'),
    path('books/<int:pk>/delete/', views.delete_book, name='delete_book/'),
]