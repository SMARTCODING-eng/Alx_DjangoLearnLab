from django.db import models
from posts.models import Userprofile, Post
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType



class Notification(models.Model):
    VERB =(
        ('FOLLOW', 'follow'),
        ('LIKE', 'like'),
        ('COMMENT', 'comment'),
    )
    recipient = models.ForeignKey(Userprofile, on_delete=models.CASCADE, related_name='notifications')
    actor = models.ForeignKey(Userprofile, on_delete=models.CASCADE, related_name='actor_notifications')
    verb = models.CharField(max_length=255, choices=VERB)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    target = GenericForeignKey('content_type', 'object_id')
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']

    
