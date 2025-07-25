from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib import messages
from django.utils.html import escape
from .models import Book
from forms import BookForm
from .forms import ExampleForm

@permission_required('app_name.can_view', raise_exception=True)
@login_required
def book_detail_view(request, book_id):
    """
    Views to display book detals.
    Requires 'can_view' permission.
    """
    if request.method == 'POST':
        if request.method == 'POST':
            form = BookForm(request.POST)
            if form.is_valid():
                book = form.save()
                messages.success(request, f'Book "{book.title}" created successfully!')
                return redirect('book_detail', book_id=book.id)
    else:
        form = BookForm()
    
    return render(request, 'books/book_form.html', {'form': form, 'action': 'Create'})
    

@permission_required('app_name.can_create', raise_exception=True)
def book_create_view(request):
    
    """
    View to create a new book.
    Requires 'can_create' permission.
    """
    if request.method == 'POST':
        try:
            title = request.POST.get('title')
            author = request.POST.get('author')
            publication_year = request.POST.get('publication_year')

            if not title or not author or not publication_year:
                raise ValueError("All fields are required")

            book = Book.objects.create(
                title=title,
                author=author,
                publication_year=publication_year
            )
            messages.success(request, f'Book "{book.title}" created successfully!')
            return redirect('book_detail', book_id=book.id)

        except Exception as e:
           messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f'Error creating book: {str(e)}')
    return render(request, 'books/book_create.html')


@permission_required('app_name.can_edit', raise_exception=True)
def book_update_view(request, book_id):
    """
    Views to edit an existing book.
    Requires 'can_edit_book' permission
    """
    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        try:
            title = request.POST.get('title')
            author = request.POST.get('author')
            publication_year = request.POST.get('publication_year')

            if not title or not author or not publication_year:
                raise ValueError("All fields are required")
            
            book.title = title
            book.author = author
            book.publication_year = publication_year
            book.save()
            messages.success(request, f'Book "{book.title}" updated successfully!')
            return redirect('book_detail', book_id=book.id)
        
        except ValueError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f'Error updating book: {str(e)}')

    return render(request, 'books/book_edit.html', {'book':book})


@permission_required('app_name.can_delete', raise_exception=True)
@login_required
def book_delete_view(request, book_id):
    """
    View to delete a book.
    Requires 'can_delete_book' permission.
    """
    book = get_object_or_404(Book, pk=book_id)
    
    if request.method == 'POST':
        title = book.title
        book.delete()
        messages.success(request, f'Book "{title}" deleted successfully!')
        return redirect('book_list')
    
    return render(request, 'books/book_confirm_delete.html', {'book': book})
