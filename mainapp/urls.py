from django.urls import path

from . import views, reports

app_name="mainapp"

urlpatterns = [
    path('kutuphane/', views.index),
    path('kutuphane/index/',views.index,name='index'),
    path('kutuphane/searchbook/', views.searchbook, name='searchbook'),
    path('kutuphane/addbook/', views.addbook, name='addbook'),
    path('kutuphane/units/', views.units, name='units'),
    #path('libraries/', views.libraries, name='libraries'),
    path('kutuphane/addreader/<str:school_num>/<str:library_entry_id>', views.addreader, name='addreader'),
    path('kutuphane/save_lending/<str:school_num>/<str:library_entry_id>', views.save_lending, name='save_lending'),
    path('kutuphane/inventory/', views.inventory, name='inventory'),
    path('kutuphane/login/', views.login, name='login'),
    path('kutuphane/users/', views.users, name='users'),
    path("kutuphane/books/<str:isbn>", views.the_book, name="book"),
    path("kutuphane/lending/<str:library_entry_id>", views.lending, name="lending"),
    path("kutuphane/success/",views.success,name="success"),
    path("kutuphane/report/", reports.report,name="report"),
    path("kutuphane/admin_report/", reports.admimistrative_report,name="admin_report"),
    path("kutuphane/which_lib/<str:isbn>",views.which_lib, name="which_lib"),
    path("kutuphane/reader_detail/<str:id>",reports.reader_detail, name="reader_detail"),
    path("kutuphane/take_back",views.take_back,name="take_back"),

]
