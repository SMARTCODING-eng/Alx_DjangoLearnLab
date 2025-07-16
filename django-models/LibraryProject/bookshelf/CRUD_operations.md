# This is the CRUD documentation


## Create

from bookshelf.models import Book

new_book = Book.objects.create(
    title="1984",
    author="George Orwell",
    published_year=1949
)


## Retrieve

book = Book.objects.get(title="1984")

## Update

book = Book.objects.get(title="1984")
book.update(title="Nineteen Eighty Four")
book.save()

## Delete

book = Book.objects.get(title="Nineteen Eighty Four")
book.delete()