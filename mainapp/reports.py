from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .forms import UnitForm, BookForm, LibraryForm, ReaderForm, LendingForm, UserForm
from .models import Book, Unit, Library, Reader, Lending
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect
from datetime import datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist


import csv



@login_required
def report(request):
    liste=[]
    header=[]
    unit=Unit.objects.get(id=request.user.username)
    if request.method == 'POST':
        selection=request.POST.get("selection")
        response = HttpResponse(content_type='"text/csv"; charset="utf-8"; dialect="excel-tab"')
        if selection=="books":
            response['Content-Disposition'] = 'attachment; filename="books.csv"'
            writer = csv.writer(response)
            writer.writerow(['ISBN', 'Kitap Adı', 'Yazar'])
            liste=Library.objects.filter(unit=Unit.objects.get(id=request.user.username)).values_list('book__isbn', 'book__title','book__writer')
            #liste = Book.objects.all().values_list('isbn', 'title', 'writer')

            header=['ISBN', 'Kitap Adı', 'Yazar']

        if selection=="readers":
            response['Content-Disposition'] = 'attachment; filename="readers.csv"'
            writer = csv.writer(response)
            writer.writerow(['okul no', 'isim', 'sınıf', "şube"])
            liste = Reader.objects.filter(unit=Unit.objects.get(id=request.user.username)).values_list('school_num','name','grade','department')
            header=['Okul No', 'İsim', 'Sınıf', "Şube"]

        if selection=="lendings":
            response['Content-Disposition'] = 'attachment; filename="lendings.csv"'
            writer = csv.writer(response)
            writer.writerow(['Okul No','İsim', 'Sınıf', 'Şube', 'ISBN', 'Kitap Adı', 'Ödünç Alma Tarihi', 'Geri Getirme Tarihi', "İade Edildi Mi"])
            lended_books = Lending.objects.filter(unit=Unit.objects.get(id=request.user.username)).values_list('reader__school_num', 'reader__name', 'reader__grade', 'reader__department',
                                                        'library_entry__book__isbn','library_entry__book__title',
                                                        'lend_date','back_date','returned')
            header=['Okul No','İsim', 'Sınıf', 'Şube', 'ISBN', 'Kitap Adı', 'Ödünç Alma Tarihi', 'Geri Getirme Tarihi', "İade Edildi Mi"]
            liste=[]
            for item in lended_books:
                item_element=[]
                for i in range(8): #ilk 7 eleman değişmeden aktarılacak, 8. boolean
                    item_element.append(item[i])
                if item[8]==True:
                    item_element.append("İade Edildi")
                else:
                    item_element.append("İade Edilmedi")
                liste.append(item_element)

        count=len(liste)

        msg=""
        if count!=0:
            msg=str(unit)+", kurumunuzda "+str(count)+" adet kayıt bulundu"
        else:
            msg=str(unit)+", kurumunuzda hiç kayıt bulunamadı..."

        return render(request, "mainapp/report.html",{"liste":liste, "header":header, "msg":msg})
    else:
        return render(request, "mainapp/report.html")
