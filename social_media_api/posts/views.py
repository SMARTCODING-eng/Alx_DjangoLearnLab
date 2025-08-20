from django.shortcuts import render
from .models import Post, Comment
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .serializers import PostSerializer, CommentSerializer
from.models import Post, Comment
from rest_framework import generics


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsAuthenticatedOrReadOnly]

    filterset_fields = ['title', 'content']
    searchset_fields = ['author', 'title', 'content']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class UserFeedView(generics.ListAPIView):
    """
    A view that returns a feed of posts from users the current user follows.
    """
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        followed_users = user.following.all()  
        queryset = Post.objects.filter(owner__in=followed_users).order_by('-created_at')
        return queryset