from django.urls import path, include

from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/<int:profile_id>/', views.profile_page, name='profile_page'),
    path('profile/<int:profile_id>/review', views.review, name='review'),
    path('inbox/', views.inbox, name='inbox'),
    path('request/<int:pk>/', views.AskDetailView.as_view(), name='ask-detail'),
    path('request/<int:pk>/delete/', views.AskDeleteView.as_view(), name='ask-delete'),
    path('request/<int:pk>/complete/', views.AskCompleteView.as_view(), name='ask-complete'),
    path('request/<int:ask_id>/accept/', views.accept_ask, name='ask-accept'),
    path('request/<int:ask_id>/decline/', views.decline_ask, name='ask-decline'),
]