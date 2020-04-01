from django.urls import path, include

from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/<int:profile_id>/', views.profile_page, name='profile_page'),
]