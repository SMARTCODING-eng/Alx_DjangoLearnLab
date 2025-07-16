# query_samples.py
from models import Author, Book, Library, Librarian

def query_script():
    author1 = Author.objects.get(name="Johnson")
    books_by_author = Book.objects.filter(author=author1)
    for book in books_by_author:
        print(f"Book Title: {book.title}")

    library1 = Library.objects.get(name="The Library")
    books_in_library = library1.books.all()
    for books in books_in_library:
        print(f"{book.title} by {book.author.name}")

    librarian1 = Librarian.objects.get(library=library1)
    print(f"Librarian for {library1.name}: {librarian1.name}")


    

   