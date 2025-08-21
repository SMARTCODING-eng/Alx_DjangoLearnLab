from django.shortcuts import render
from .models import Post, Comment
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.db.utils import IntegrityError
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from.models import Post, Comment, Like
from rest_framework import generics


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAuthenticatedOrReadOnly]

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


    def perform_create(self, serializer):
        try:
            serializer.save(author=self.request.user)
        except IntegrityError:
            return Response(
                {"error": "You have already liked this post."},
                status=status.HTTP_409_CONFLICT
            )
