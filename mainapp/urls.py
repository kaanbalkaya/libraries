from django.urls import path

from . import views

app_name="mainapp"

urlpatterns = [
    path('', views.index),
    path('index/',views.index,name='index'),
    path('searchbook/', views.searchbook, name='searchbook'),
    path('addbook/', views.addbook, name='addbook'),
    path('units/', views.units, name='units'),
    path('libraries/', views.libraries, name='libraries'),
    path('addreader/<str:unit_id>/<str:school_num>/<str:library_entry_id>', views.addreader, name='addreader'),
    path('inventory/', views.inventory, name='inventory'),
    path('login/', views.login, name='login'),
    path('users/', views.users, name='users'),
    path("books/<str:isbn>", views.the_book, name="book"),
    path("lending/<str:library_entry_id>", views.lending, name="lending"),
    path("success/",views.success,name="success"),
    path("report/", views.report,name="report"),
]
