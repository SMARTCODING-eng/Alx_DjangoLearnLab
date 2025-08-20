from django.db import models
from django.contrib.auth.models import AbstractUser


class Userprofile(AbstractUser):
    username = models.CharField(max_length=150, default='email', unique=True)
    email = models.EmailField(max_length=150, unique=True)
    password = models.CharField(max_length=50)
    bio = models.TextField(max_length=250, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True)
    follower = models.ManyToManyField('self', symmetrical=False, related_name='followings', blank=True)
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='userprofile_groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_query_name='Userprofile',
    )
    user_permissions = models.ManyToManyField(
        'auth.permission',
        related_name='userprofile_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='Userprofile',
    )

