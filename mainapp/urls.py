from django.urls import path

from . import views, reports

app_name="mainapp"

urlpatterns = [
    path('', views.index),
    path('index/',views.index,name='index'),
    path('searchbook/', views.searchbook, name='searchbook'),
    path('addbook/', views.addbook, name='addbook'),
    path('units/', views.units, name='units'),
    path('libraries/', views.libraries, name='libraries'),
    path('addreader/<str:school_num>/<str:library_entry_id>', views.addreader, name='addreader'),
    path('save_lending/<str:school_num>/<str:library_entry_id>', views.save_lending, name='save_lending'),
    path('inventory/', views.inventory, name='inventory'),
    path('login/', views.login, name='login'),
    path('users/', views.users, name='users'),
    path("books/<str:isbn>", views.the_book, name="book"),
    path("lending/<str:library_entry_id>", views.lending, name="lending"),
    path("success/",views.success,name="success"),
    path("report/", reports.report,name="report"),
    path("which_lib/<str:isbn>",views.which_lib, name="which_lib"),
    path("take_back",views.take_back,name="take_back"),
]
