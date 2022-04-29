from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .forms import UnitForm, BookForm, LibraryForm, ReaderForm, LendingForm, UserForm
from .models import Book, Unit, Library, Reader, Lending
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect
from datetime import datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist
import csv

def register_book(book, unit, description=""):
    try:
        library_entry=Library.objects.filter(unit=unit).get(book=book)
        #kitap varsa sayısını bir artır
        library_entry.amount=library_entry.amount+1
    except Exception as e:
        #ancak kitap yoksa yeni bir kayıt oluştur
        library_entry=Library(unit=unit,book=book)

    library_entry.description=description
    library_entry.save()
    return library_entry

def index(request):
    msg=""
    units=Unit.objects.all()
    liste=None
    lib_set=None
    if request.method=="POST":
        search_type=request.POST.get("search_type")
        search_text=request.POST.get("search_text")
        which_unit=request.POST.get("which_unit")

        if which_unit=="all" and search_text!="":
            if search_type=="isbn":
                liste=Book.objects.filter(isbn__contains=search_text)
            elif search_type=="title":
                liste=Book.objects.filter(title__contains=search_text)
            elif search_type=="writer":
                liste=Book.objects.filter(writer__contains=search_text)
        elif which_unit=="all" and search_text=="":
            msg="Ne arıyorsunuz?"
            liste=Book.objects.all()
        elif which_unit!="all" and search_text!="":
            the_library=Library.objects.filter(unit=Unit.objects.get(id=which_unit))
            book_list=None

            if search_type=="isbn":
                book_list=list(Book.objects.filter(isbn__contains=search_text))
            elif search_type=="title":
                book_list=list(Book.objects.filter(title__contains=search_text))
            elif search_type=="writer":
                book_list=list(Book.objects.filter(writer__contains=search_text))
            lib_set=the_library.filter(book__in = book_list)
        elif which_unit!="all" and search_text=="":
            the_library=Library.objects.filter(unit=Unit.objects.get(id=which_unit))
            msg=str(which_unit)+" kütüphanesinde ne arıyorsunuz? "
            lib_set=the_library.all()
        else:
            liste=Book.objects.all()

    else:
        liste=Book.objects.all()

    return render(request,'mainapp/index.html', {'liste':liste, 'msg':msg, 'units':units, 'lib_set':lib_set})

@login_required
def success(request):
    return render(request,"mainapp/success.html")


@login_required
def searchbook(request):
    msg=""
    if request.method=="POST":
        search=request.POST.get("search_text")
        #kitap kayıtlarda varsa;
        liste=Book.objects.filter(isbn=search)
        if not liste:
            return redirect("/addbook")
    else:
        liste=Book.objects.all()
    return render(request,'mainapp/searchbook.html',{'liste':liste, 'title':'Kitap Ara', 'msg':msg})

@login_required
def addbook(request):
    msg=""
    if request.method == 'POST':
        formset = BookForm(request.POST)
        if formset.is_valid():
            book=formset.save()
            description=request.POST.get("description")
            register_book(book,Unit.objects.get(id=request.user.username), description)
            return redirect("/success")

    else:
        msg="Aradığınız kitap bulunamadı, Eklemek için aşağıdaki formu doldurunuz."
        formset=BookForm()
    return render(request,'mainapp/addbook.html', {'formset':formset, 'msg':msg})






@login_required
def inventory(request):
    ##kitapları kütüphane girişlerinden süzüp getir
    liste=Library.objects.filter(unit=Unit.objects.get(id=request.user.username))

    if request.method=="POST":
        search_text=request.POST.get("search_text")
        try:
            liste=liste.filter(book=Book.objects.get(isbn=search_text))
        except Exception as e:
            ##lan oğlum böyle olmaz
            #liste boşsa boştur orjinali aramadan önceki halini gösteririz
            pass
    return render(request,'mainapp/inventory.html', {'liste':liste})


def which_lib(request, isbn):
    try:
        book=Book.objects.get(isbn=isbn)
    except ObjectDoesNotExist:
        return redirect("/index")
    liste=Library.objects.filter(book=book)
    units=[]
    for l in liste:
        units.append(l.unit)
    return render(request,'mainapp/which_lib.html', {'book':book, 'units':units})

@login_required
def save_lending(request,school_num,library_entry_id):
    unit_id=request.user.username
    reader_id=unit_id+'-'+school_num

    try:
        reader=Reader.objects.get(id=reader_id)
        library_entry=Library.objects.get(id=library_entry_id)
        if request.method=='POST':
            library_entry.on_lending+=1
            library_entry.save()
            reader.books_lended+=1
            reader.save()
            l=Lending(unit=Unit.objects.get(id=request.user.username),
                                            reader=reader,
                                            library_entry=library_entry,
                                            lend_date=datetime.now().strftime("%Y-%m-%d"),
                                            back_date=(datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d"))
            l.save()
            return redirect("/success")

    except ObjectDoesNotExist:
        url="/lending/"+library_entry_id
        return redirect(url)

    return render(request, 'mainapp/lending_summary.html',{'library_entry':library_entry,'reader':reader})


@login_required
def addreader(request, school_num, library_entry_id):
    msg="Kayıt Giriniz."
    formset=ReaderForm()
    unit_id=request.user.username
    reader_id=unit_id+'-'+school_num
    library_entry=Library.objects.get(id=library_entry_id)
    if request.method == 'POST':
        formset = ReaderForm(request.POST)
        if formset.is_valid():
            if Reader.objects.filter(id=reader_id).exists():
                msg="kullanıcı zaten kayıtlı"
                formset=ReaderForm()
            else:
                reader=formset.save(commit=False)
                reader.unit=Unit.objects.get(id=unit_id)
                reader.id=reader_id
                reader.school_num=school_num
                reader.save()
                url="/save_lending/"+school_num+"/"+library_entry_id
                return redirect(url)

    return render(request,'mainapp/adduser.html',{'library_entry':library_entry,
                                                    'formset':formset,
                                                    'title':'addreader',
                                                    'msg':msg})


@login_required
def lending(request,library_entry_id):
    library_entry=Library.objects.get(id=library_entry_id)

    if request.method == 'POST':
        school_num=request.POST.get("school_num")
        unit_id=request.user.username
        reader_id=unit_id+'-'+school_num
        try:
            reader=Reader.objects.get(id=reader_id)
            url="/save_lending/"+school_num+"/"+library_entry_id
            return redirect(url)
        except ObjectDoesNotExist:
            url="/addreader/"+school_num+"/"+library_entry_id
            return redirect(url)
    else:
        return render(request,'mainapp/lending.html', {'library_entry':library_entry})


@login_required
def take_back(request):
    msg=""
    unit_id=request.user.username
    lendings=Lending.objects.filter(unit=Unit.objects.get(id=unit_id)).filter(returned=False)
    ### TODO: kullanıcı araması için bir inputtan bilgi al
    ### kullanıcıyı bul, yoksa yaratılacak formu göster
    if request.method == 'POST':
        school_num=request.POST.get("school_num")
        if school_num:
            try:
                lendings=Lending.objects.filter(reader=Reader.objects.filter(unit_id=unit_id).get(school_num=school_num))
            except ObjectDoesNotExist:
                msg="Aradığınız kayıt bulunamadı..."
                pass
        lending_id=request.POST.get("lending_id")
        if lending_id:

            l=Lending.objects.get(id=lending_id)
            l.returned=True
            l.library_entry.on_lending-=1
            l.library_entry.save()
            l.save()
            msg="iade alındı..."
    return render(request,'mainapp/take_back.html', {'lendings':lendings, 'msg':msg})



def login(request):
    return render(request,'mainapp/login.html')

@user_passes_test(lambda user:user.is_staff )
def users(request):
    if request.method == 'POST':
        formset = UserForm(request.POST)
        if formset.is_valid():
            formset.save()
            formset=UserForm()
    else:
        formset=UserForm()
    return render(request,'mainapp/formset.html',{'formset':formset,'title':'users'})

@user_passes_test(lambda user:user.is_superuser)
def units(request):
    msg="Kayıt Giriniz."
    if request.method == 'POST':
        formset = UnitForm(request.POST)
        if formset.is_valid():
            formset.save()
            msg="Kayıt başarılı."
            formset=UnitForm()
    else:
        formset=UnitForm()
    return render(request,'mainapp/formset.html',{'formset':formset, 'msg':msg})

@user_passes_test(lambda user:user.is_superuser)
def libraries(request):
    msg="Kayıt Giriniz."
    if request.method == 'POST':
        formset = LibraryForm(request.POST)
        if formset.is_valid():
            formset.save()
            msg="Kayıt başarılı."
            formset=LibraryForm()
    else:
        formset=LibraryForm()
    return render(request,'mainapp/formset.html',{'formset':formset,'title':'libraries', 'msg':msg})


@login_required
def the_book(request,isbn):
    book=Book.objects.get(isbn=isbn)
    if request.method == 'POST':
        description=request.POST.get("description")
        register_book(book,Unit.objects.get(id=request.user.username),description)
        return redirect("/success")
    return render(request,'mainapp/book.html', {'book':book})


def error_404_view(request, exception):
    return render(request,'mainapp/error_404.html', {"name": "ThePythonDjango.com"})
