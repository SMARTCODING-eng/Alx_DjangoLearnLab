from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from taggit.managers import TaggableManager

class CustomUser(AbstractBaseUser):
    bio = models.TextField(blank=True, null=True)
    username = None
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateField(auto_now_add=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')
    tags = TaggableManager()

    def __str__(self):
        return f'Post: {self.title} by {self.author.email}'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='Comment')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'comment by {self.author.email} on {self.post.title}.'



