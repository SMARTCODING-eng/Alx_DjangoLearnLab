# Update the book name

book = Book.objects.get(title="1984")
book.update(title="Nineteen Eighty-Four")
book.save()

print(f"Successfully update book.title from '1984' to {book.title} ")

output:

<!-- Successfully update book.title from '1984' to "Nineteen Eighty-Four" -->
