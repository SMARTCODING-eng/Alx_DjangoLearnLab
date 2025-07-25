from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('email is required')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(username, email, password, **extra_fields)
    
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Custom User'
        verbose_name_plural = 'Custom Users'

    def __str__(self):
        return self.username


class Book(models.Model):
    title = models.CharField(max_length=200, unique=True)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

    class Meta:
        permissions = [
            ("can_view", "can view details of books"),
            ("can_create", "can create books"),
            ("can_edit", "can edit books"),
            ("can_delete", "can delete books"),
        ]


    def __str__(self):
        return f"{self.title} by {self.author} ({self.publication_year})"


class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('Admin', 'Admin'),
        ('Librarian', 'Librarian'),
        ('Member', 'Member'),
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='User'
        )
    

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Member')
    bio = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"{self.user.username} ({self.role})"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_user_groups()

    def update_user_groups(self):
        """update the user's groups based on their role"""
        self.user.groups.clear()
        if self.role == 'Admin':
            group, _ = Group.objects.get_or_create(name='Admin')
            self.user.groups.add(group)
            self.user.is_staff = True
            self.user.save()

        elif self.role == 'Librarian':
            group, _ = Group.objects.get_or_create(name='Editors')
            self.user.groups.add(group)
            self.assign_permissions_to_group('Editors', [
                'can_view',
                'can_create',
                'can_edit',
            ])
            self.user.save()
        elif self.role == 'Member':
            group, _ = Group.objects.get_or_create(name='Viewers')
            self.user.groups.add(group)
            self.assign_permissions_to_group('Viewers', [
                'can_view',
            ])
    @staticmethod
    def assign_permissions_to_group(group_name, permission_codenames):
        """"assigning permissions to the groups"""
        group = Group.objects.get(name=group_name)
        content_type = ContentType.objects.get_for_model(Book)
        
        for codename in permission_codenames:
            permission = permission.objects.get(
                content_type=content_type,
                codename=codename
            )
            group.permissions.add(permission)


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()




    

