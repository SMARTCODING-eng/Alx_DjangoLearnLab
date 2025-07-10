# Retriving the book created 

book = Book.objects.get(title="1984")
**Retrieving all the artibute**
print(f"Title: {book.title}")
print(f"Author: {Book.author}")
print(f"Publication year: {book.published_year})

<!-- python -->

output:
<!-- 
Tile: 1984
Author: George Orwell
Publication year: 1949 --> -->