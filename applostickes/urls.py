from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('about/', views.about, name='about'),
    path('user/', views.user, name='user'),
    path('groups/', views.groups, name='groups'),
    path('debts/', views.debts, name='debts'),
    path('create/', views.createGroup, name='createGroup'),
]