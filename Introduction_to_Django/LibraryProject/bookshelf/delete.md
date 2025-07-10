# Delete the book

book = Book.objects.get(title="Nineteen Eighty Four")
book.delete()


print("Book deleted successfully")

<!-- python -->

output  