# Create Book

**This is the documentation of the book creations**
from bookshelf.models import Book

new_book = Book.objects.create(
    title="1984",
    author="George Orwell",
    published_year=1949
)
print(f"Book: (Titled:{new_book.title} by {new_book.author} published in {new_book.published_year}) was created Successfully")

<!-- python -->

<!-- Output:

Book: (Titled:1984 by George Orwell published in 1949 was created Successfully) -->