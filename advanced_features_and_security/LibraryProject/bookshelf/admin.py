from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Book, UserProfile, CustomUser
from django.utils.translation import gettext_lazy as _


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'username', 'date_of_birth', 'is_staff')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('personal_info'), {'fields': ('username', 'date_of_birth', 'profile_photo')}),
        (_('permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('important_date'), {'fields': ('last_logins', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields' : ('email', 'username', 'date_of_birth', 'password1', 'password2'), 
        }),
    )
    search_fields = ('email', 'username')
    ordering = ('email',)


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
    search_fields = ('title', 'author')
    list_filter = ('publication_year',)
    ordering = ('title',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(UserProfile)

