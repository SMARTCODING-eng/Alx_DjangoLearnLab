from django.urls import path, include
from . import views

urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('follow/<int:user_id>/', views.FollowUserView.as_view(), name='follow'),
    path('unfollow/<int:user_id>/', views.FollowUserView.as_view(), name='unfollow'),
    path("", views.good_day, name="good_day")
]

