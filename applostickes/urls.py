from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('about/', views.about, name='about'),
    path('user/', views.user, name='user'),
    path('groups/', views.groups, name='groups'),
    path('debts/', views.debts, name='debts'),
    path('createGroup/', views.createGroup, name='createGroup'),
    path('createDebt/', views.createDebt, name='createDebt'),
    path('group/<str:groupName>-<str:group_identifier>', views.group, name='group'),
    path('debt/<str:debtName>-<str:transaction_identifier>', views.debt, name='debt'),
]