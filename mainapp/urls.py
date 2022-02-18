from django.urls import path

from . import views

app_name="mainapp"

urlpatterns = [
    path('', views.index),
    path('index/',views.index,name='index'),
    path('books/', views.books, name='books'),
    path('units/', views.units, name='units'),
    path('libraries/', views.libraries, name='libraries'),
    path('readers/', views.readers, name='readers'),
    path('lendings/', views.lendings, name='lendings'),
    path('login/', views.login, name='login'),
    path('users/', views.users, name='users'),
]
