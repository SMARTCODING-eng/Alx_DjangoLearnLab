from django.shortcuts import render
from .models import Author, Book, Library, Librarian




def books_by_author(requests, author_name):
    author = Author.objects.get(name=author_name)
    books = Book.objects.filter(author=author)
    return render(requests, 'books_by_author.html', {'author': author, 'books': books})




