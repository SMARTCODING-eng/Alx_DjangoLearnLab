from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=200)




class Book(models.Model):
    title = models.CharField(max_length=50)
    publication_year = models.DateField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='Books')



