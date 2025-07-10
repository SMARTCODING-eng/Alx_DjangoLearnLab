from django.contrib import admin
from .models import Book

# Register your models here.

# Register the Book model with the admin site
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_year')
    search_fields = ('title', 'author')
    list_filter = ('author', 'published_year')
    ordering = ('title',)
    

admin.site.register(Book, BookAdmin)

