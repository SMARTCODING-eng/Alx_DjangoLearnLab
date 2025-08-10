from django.shortcuts import render
from rest_framework import generics, status
from .models import Book
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .serializers import BookSerializer
from datetime import datetime
from django_filters import rest_framework
 

class ListView(generics.ListAPIView):
    """A view that list all the books in the 
    Library
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    


class DetailView(generics.RetrieveAPIView):
    """
    A  view that retrieve all  the details if a
    particular book
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_by = filters.OrderingFilter


class CreateView(generics.CreateAPIView):
    """
    A View that handles the creation of a book instance
    by an authenticated user
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        publication_year = serializer.validated_data.get('publication_year')
        if publication_year > datetime.now().year:
            raise serializer.ValidationError("Invalid publication Year")
        serializer.save()        


class UpdateView(generics.UpdateAPIView):
    """
    A view that Handles The Update of book instances
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        publication_year = serializer.validated_data.get('publication_year')
        if publication_year > datetime.now().year:
            raise serializer.ValidationError("Invalid Publication year")
        serializer.save()


class DeleteView(generics.DestroyAPIView):
    """
    A view that handle the deletion of a book instance
    by an authenticated user.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, serializer):
        serializer.instance.delete()
        serializer.save()
