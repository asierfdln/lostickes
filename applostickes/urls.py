from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('user/', views.user, name='user'),
    path('group/', views.group, name='group'),
    path('debt/', views.debt, name='debt'),
    path('create/', views.createGroup, name='createGroup'),
]