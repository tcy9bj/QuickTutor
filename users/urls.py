from django.urls import path, include

from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/<int:profile_id>/', views.profile_page, name='profile_page'),
    path('inbox/', views.inbox, name='inbox'),
    path('request/<int:pk>', views.AskDetailView.as_view(), name='ask-detail'),
    path('request/<int:pk>/delete', views.AskDeleteView.as_view(), name='ask-delete')
]