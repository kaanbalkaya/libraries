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
    if request.method == 'POST':
        selection=request.POST.get("selection")
        response = HttpResponse(content_type='"text/csv"; charset="utf-8"; dialect="excel-tab"')
        if selection=="books":
            response['Content-Disposition'] = 'attachment; filename="books.csv"'
            writer = csv.writer(response)
            writer.writerow(['isbn', 'başlık', 'yazar'])
            items = Book.objects.all().values_list('isbn', 'title', 'writer')

        if selection=="readers":
            response['Content-Disposition'] = 'attachment; filename="readers.csv"'
            writer = csv.writer(response)
            writer.writerow(['okul no', 'isim', 'sınıf', "şube"])
            items = Reader.objects.filter(unit=Unit.objects.get(id=request.user.username)).values_list('school_num','name','grade','department')

        if selection=="lendings":
            response['Content-Disposition'] = 'attachment; filename="lendings.csv"'
            writer = csv.writer(response)
            writer.writerow(['Okul No','isim', 'Sınıf', 'Şube', 'isbn', 'Kitap Adı', 'Ödünç Alma Tarihi', 'Geri Getirme Tarihi'])
            items = Lending.objects.filter(unit=Unit.objects.get(id=request.user.username)).values_list('reader__school_num', 'reader__name', 'reader__grade', 'reader__department',
                                                        'library_entry__book__isbn','library_entry__book__title',
                                                        'lend_date','back_date','returned')

        return render(request, "mainapp/report.html",{"items":items})
    else:
        return render(request, "mainapp/report.html")
