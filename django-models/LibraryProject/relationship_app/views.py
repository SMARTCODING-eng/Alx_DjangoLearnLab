from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.detail import DetailView
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.decorators import permission_required
from django import forms
from .models import Library
from .models import Book, Author
from .forms import UserRegistrationForm

def is_admin(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def is_librarian(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_member(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Member'

def list_books(request):
    books = Book.objects.all().select_related('author')
    context = {
        'books': books
    }
    return render(request, 'relationship_app/list_books.html', context)


class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = self.object.books.all().select_related('author')
        return context


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('relationship_app:list_books')
        
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('relationship_app:list_books')
            else:
                form.add_error(None, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'relationship_app/login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return redirect('relationship_app:list_books')
    


@login_required
@user_passes_test(is_admin, login_url='/relationship_app/login/')
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html', {'user': request.user})

@login_required
@user_passes_test(is_librarian, login_url='relationship_app/login/')
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html', {'user': request.user})

@login_required
@user_passes_test(is_member, login_url='relationship_app/login/')
def member_view(request):
    return render(request, 'relationship_app/member_view.html', {'user': request.user})



class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author']


    
@login_required
@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('relationship_app:list_books')
    else:
        form = BookForm
    return render(request, 'relationship_app/add_book.html', {'form': form, 'user': request.user})


@login_required
@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('relationship_app:list_books')
        else:
            form = BookForm(instance=book)
        return render(request, 'relationship_app/edit_book.html', {'form': form, 'book': book, 'user': request.user})



@login_required
@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('relationship_app/list_books')
    return render(request, 'relationship_app/delete_book_confirm.html', {'book': book, 'user': request.user})
