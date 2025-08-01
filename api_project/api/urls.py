from django.urls import path, include
from .views import BookList, BookViewSet
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'books_all', BookViewSet, basename='books_all')


app_name = 'api'

urlpatterns = [
    # path('books/', BookList.as_view(), name='book-list'),
    # path('', BookList.as_view(), name='book-list'),
    path('', include(router.urls))
]