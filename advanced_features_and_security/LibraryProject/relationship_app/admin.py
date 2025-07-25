from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile, Author, Book, Library, Librarian, CustomUser
from django.utils.translation import gettext_lazy as _

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = [
        'username', 'email', 'first_name', 'last_name', 'date_of_birth', 'is_staff'
    ]
    fieldsets = UserAdmin.fieldsets + (
        (_('Additional Info'), {
            'fields': ('date_of_birth', 'profile_photo'),
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
         (_('Additional Info'), {
            'fields': ('date_of_birth', 'profile_photo'),
        }),

    )
    list_filter = UserAdmin.list_filter + ('date_of_birth',)
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ['username',]

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserProfile)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Library)
admin.site.register(Librarian)