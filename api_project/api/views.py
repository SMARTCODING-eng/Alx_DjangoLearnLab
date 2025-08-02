from django.shortcuts import render
from rest_framework import generics
from .models import Book
from .serializers import BookSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated


class UserViewSet(viewsets.ModelViewSet):
    """
    This class gave full permission
    on who can use the app
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_permissions(self):
        """
        This is give access and restrict
        all user who are not authenticated
        only authenticated and adminuser 
        can perform operations on the app
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
            return [permission() for permission in permission_classes]



class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    

class BookViewSet(viewsets.ModelViewSet):
    """This get all the Items of the book"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
