# from django.shortcuts import generic
from .models import Post, Comment
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.db.utils import IntegrityError
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from.models import Post, Comment, Like
from rest_framework import generics
from notifications.models import Notification


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    filterset_fields = ['title', 'content']
    searchset_fields = ['author', 'title', 'content']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class UserFeedView(generics.ListAPIView):
    """
    A view that returns a feed of posts from users the current user follows.
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        following_users = user.following.all()  
        queryset = Post.objects.filter(author__in=following_users).order_by('-created_at')
        return queryset

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]


    def perform_create(self, request, *args, **kwargs):
        pk = request.data.get('post')
        if not pk:
            return Response({"error": "Post ID required."}, status=status.HTTP_400_BAD_REQUEST)
        post = generics.get_object_or_404(Post, pk=pk)
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if not created:
            return Response({"error": "You have already liked this post."}, status=status.HTTP_409_CONFLICT)
        

        Notification.objects.create(
            sender=request.user,
            recipient=post.author,
            notification_type='LIKE',
            post=post
        )

        serializer = self.get_serializer(like)
        return Response(serializer.data, status=status.HTTP_201_CREATED)