from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .forms import UnitForm, BookForm, LibraryForm, ReaderForm, LendingForm, UserForm
from .models import Book, Unit, Library, Reader, Lending
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect
from datetime import datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist
#import csv

@user_passes_test(lambda user:user.is_superuser)
def admimistrative_report(request):
    liste=[]
    header=[]
    units=Unit.objects.all()
    selection=""
    if request.method=="POST":
        which_unit=request.POST.get("which_unit")

        if which_unit=="all":
            selection=request.POST.get("selection")
            if selection=="books":
                liste=Library.objects.all().values_list('book__isbn', 'book__title','book__writer')
                header=['ISBN', 'Kitap Adı', 'Yazar']

            if selection=="readers":
                liste = Reader.objects.all().order_by("-books_lended").values('id','school_num','name','grade','department','books_lended')
                header=['Okul No', 'İsim', 'Sınıf', 'Şube', 'Ödünç Alınan Kitaplar']

            if selection=="lendings":
                lended_books = Lending.objects.all().values_list('reader__school_num', 'reader__name', 'reader__grade', 'reader__department',
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

        else:
            selection=request.POST.get("selection")
            if selection=="books":
                liste=Library.objects.filter(unit=Unit.objects.get(id=which_unit)).values_list('book__isbn', 'book__title','book__writer')
                header=['ISBN', 'Kitap Adı', 'Yazar']

            if selection=="readers":
                liste = Reader.objects.filter(unit=Unit.objects.get(id=which_unit)).order_by("-books_lended").values('id','school_num','name','grade','department', 'books_lended')
                header=['Okul No', 'İsim', 'Sınıf', 'Şube', 'Ödünç Alınan Kitaplar']

            if selection=="lendings":
                lended_books = Lending.objects.filter(unit=Unit.objects.get(id=which_unit)).values_list('reader__school_num', 'reader__name', 'reader__grade', 'reader__department',
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

        '''
        if request.POST.get("download_report"):
            response = HttpResponse(content_type='"text/csv"; charset="utf-8"; dialect="excel-tab"')
            writer = csv.writer(response)
            writer.writerow(header)
            for l in liste:
                writer.writerow(l)
            response['Content-Disposition'] = 'attachment; filename="rapor.csv"'
            return response
        '''
        return render(request, "mainapp/admin_report.html",{"liste":liste, "header":header,  "units":units, "selection":selection})
    else:
        return render(request, "mainapp/admin_report.html",{"units":units})




@login_required
def report(request):
    liste=[]
    header=[]
    unit=Unit.objects.get(user=request.user)
    selection=""

    if request.method == 'POST':
        selection=request.POST.get("selection")
        if selection=="books":
            liste=Library.objects.filter(unit=Unit.objects.get(id=request.user.username)).values_list('book__isbn', 'book__title','book__writer')
            header=['ISBN', 'Kitap Adı', 'Yazar']

        if selection=="readers":
            liste = Reader.objects.filter(unit=unit).order_by("-books_lended").values('id','school_num','name','grade','department', "books_lended")
            header=['Okul No', 'İsim', 'Sınıf', "Şube", "Ödünç Alınan Kitaplar"]

        if selection=="lendings":
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
        '''
        if request.POST.get("download_report"):
            response = HttpResponse(content_type='"text/csv"; charset="utf-8"; dialect="excel-tab"')
            writer = csv.writer(response)
            writer.writerow(header)
            for l in liste:
                writer.writerow(l)
            response['Content-Disposition'] = 'attachment; filename="rapor.csv"'
            return response
        '''

        return render(request, "mainapp/report.html",{"liste":liste, "header":header, "msg":msg,  "selection":selection})
    else:
        return render(request, "mainapp/report.html")

@login_required
def reader_detail(request,id):
    try:
        reader=Reader.objects.get(id=id)
    except ObjectDoesNotExist:
        return redirect("/report")
    liste = Lending.objects.filter(reader=reader).values('library_entry__book__isbn','library_entry__book__title', 'lend_date','back_date')
    header=['ISBN', 'Kitap Adı', 'Ödünç Alma Tarihi', 'Geri Getirme Tarihi']
    return render(request, "mainapp/reader_detail.html",{"liste":liste,"reader":reader, "header":header})
