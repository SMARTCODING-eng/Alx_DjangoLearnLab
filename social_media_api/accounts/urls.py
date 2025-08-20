from django.urls import path, include
from .views import FollowUserView, UserRegistrationView, UserLoginView, UserProfileView


urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('follow/<str:username>/', FollowUserView.as_view(), name='follow'),
    path('unfollow/<str:username>/', FollowUserView.as_view(), name='unfollow'),
]

