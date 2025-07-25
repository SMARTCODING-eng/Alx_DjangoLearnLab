# query_samples.py
from models import Author, Book, Library, Librarian

def query_script(author_name, library_name):
    author = Author.objects.get(name=author_name)
    books_by_author = Book.objects.filter(author=author)
    for book in books_by_author:
        print(f"Book Title: {book.title}")

    library1 = Library.objects.get(name=library_name)
    books_in_library = library1.books.all()
    print(f"\nBooks available in {library_name}")
    for book in books_in_library:
        print(f"{book.title} by {book.author.name}")

    librarian1 = Librarian.objects.get(library=library1)
    print(f"\nLibrarian for {library_name}: {librarian1.name}")
