from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import UnitForm, BookForm, LibraryForm, ReaderForm, LendingForm, UserForm
from .models import Book, Unit, Library, Reader, Lending
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect
from datetime import datetime, timedelta

def register_book(book, unit, description=""):
    try:
        library_entry=Library.objects.filter(unit=unit).get(book=book)
        library_entry.amount=library_entry.amount+1
    except Exception as e:
        library_entry=Library(unit=unit,book=book)

    library_entry.description=description
    library_entry.save()
    return library_entry

def index(request):
    if request.method=="POST":
        search=request.POST.get("search_text")
        liste=Book.objects.filter(title__contains=search)
    else:
        liste=Book.objects.all()
    return render(request,'mainapp/index.html', {'liste':liste})

def create_reader():

    pass

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

    else:
        msg="Aradığınız kitap bulunamadı, eklemek için aşağıdaki formu doldurun."
        formset=BookForm()
    return render(request,'mainapp/addbook.html', {'formset':formset, 'msg':msg})



@login_required
def readers(request):
    msg="Kayıt Giriniz."
    if request.method == 'POST':
        formset = ReaderForm(request.POST)
        if formset.is_valid():
            #username ve kurum kodları aynı, aktif kullanıcının adı üzerinden
            #ilgili kuruma ulaşabiliyoruz
            #istisnası admin
            unit_id=request.user.username
            school_num=formset.cleaned_data["school_num"]
            id=unit_id+'-'+school_num
            if Reader.objects.filter(id=id).exists():
                msg="kullanıcı zaten kayıtlı"
                formset=ReaderForm()
            else:
                reader=formset.save(commit=False)
                reader.unit=Unit.objects.get(id=unit_id)
                reader.id=id
                reader.save()
    else:
        formset=ReaderForm()
    return render(request,'mainapp/formset.html',{'formset':formset,'title':'readers', 'msg':msg})



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
            pass
    return render(request,'mainapp/inventory.html', {'liste':liste})

@login_required
def lending(request,id):

    library_entry=Library.objects.get(id=id)
    ### TODO: kullanıcı araması için bir inputtan bilgi al
    ### kullanıcıyı bul, yoksa yaratılacak formu göster
    if request.method == 'POST':
        reader_id=request.user.username+'-'+request.POST.get("school_num")
        try:
            reader=Reader.objects.get(id=reader_id)
        except Exception as e:
            reader=create_reader()
        l=Lending(unit=Unit.objects.get(id=request.user.username),
                                        reader=reader,
                                        library_entry=library_entry,
                                        lend_date=datetime.now().strftime("%Y-%m-%d"),
                                        back_date=(datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d"))
        l.save()
    return render(request,'mainapp/lending.html', {'library_entry':library_entry})


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

    return render(request,'mainapp/book.html', {'book':book})
