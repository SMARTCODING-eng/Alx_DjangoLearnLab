from rest_framework import serializers
from datetime import datetime
from .models import Author, Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        field = [
            'id',
            'title',
            'publication_year' 
        ]

    def validate_publication_year(self, value):
        """Custom value to ensure that
        the publication year is not in the future
        """
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError("publication year cannot be in the future.")
        return value



class AuthorSerializer(serializers.ModelSerializer):
    """The code below create a nested books"""
    books =BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        field = ['id', 'name', 'books']


    