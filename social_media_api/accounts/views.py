from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer
from rest_framework.views import APIView
from django.contrib.auth import authenticate, get_user_model
from rest_framework.authtoken.models import Token
from rest_framework import permissions


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        user = serializer.save()
        return Response({
            "user": {
                "id": user.id,
                "email": user.email
            },
            "message": "User created successfully."
        }, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            return Response({
                "id": user.id,
                "email": user.email
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        

class FollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, username):
        CustomUser = get_user_model()
        try:
            user_to_follow = CustomUser.objects.all()
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
        if request.user.following.add(user_to_follow):
            return Response({"Message": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        
        request.user.following.add(user_to_follow)
        return Response({"Message": f"You are now folloeing {username}."}, status=status.HTTP_200_OK)
    
    def unfollow_user(self, request, username):
        CustomUser = get_user_model()
        try:
            user_to_unfollow = CustomUser.objects.all()
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
        if not request.user.following.filter(username=username).exists():
            return Response({"error": f"You are not following {username}."}, status=status.HTTP_400_BAD_REQUEST)
        
        request.user.following.remove(user_to_unfollow)
        return Response({"message": f"You have unfollowed {username}."})
        
