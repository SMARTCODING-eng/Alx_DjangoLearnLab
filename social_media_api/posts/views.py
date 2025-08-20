from django.shortcuts import render
from .models import Post, Comment
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .serializers import PostSerializer, CommentSerializer
from.models import Post, Comment


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
