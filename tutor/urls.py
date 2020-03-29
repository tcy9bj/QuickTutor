from django.urls import path, include

from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('home/', views.home, name='home'),
    path('login/', views.login, name='login'),
    #path('login/', views.LoginView.as_view(), name='login'),

    #google login
    path('accounts/', include('allauth.urls')),
]