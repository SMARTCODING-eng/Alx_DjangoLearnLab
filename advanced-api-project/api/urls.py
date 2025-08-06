from django.urls import path
from .views import (
    ListView, DetailView, CreateView,
    UpdateView, DeleteView
)



urlpatterns = [
    path('books/', ListView.as_view(), name='book-list'),
    path('books-create/', CreateView.as_view(), name='book-create'),
    path('books/<int:pk>/', UpdateView.as_view(), name='book-detal'),
    path('books/<int:pk>/update/', UpdateView.as_view(), name='book-update'),
    path('books/<int:pk>/delete/', DeleteView.as_view(), name='book-delete'),

]