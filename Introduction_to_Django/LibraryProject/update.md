# Update the book name

book = Book.objects.get(title="1984")
book.update(title="Nineteen Eighty Four")
book.save()

print(f"Updated successfully")