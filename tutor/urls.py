from django.urls import path, include

from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('home/', views.home, name='home'),
    path('activate/<int:profile_id>/', views.activate, name='activate'),
    path('deactivate/<int:profile_id>/', views.deactivate, name='deactivate'),
    path('login/', views.login, name='login'),
    #path('login/', views.LoginView.as_view(), name='login'),

    #google login
    path('accounts/', include('allauth.urls')),

    #request form
    path('request/<int:tutor_id>/', views.request, name='request')
]
