from django.shortcuts import render
from django.http import HttpResponseRedirect
from .formsets import UnitForm, BookForm, LibraryForm, ReaderForm, LendingForm, UserForm
from .models import Book, Unit, Library, Reader, Lending
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect

# Create your views here.
def index(request):
    if request.method=="POST":
        search=request.POST.get("search_text")
        liste=Book.objects.filter(title__contains=search)
    else:
        liste=Book.objects.all()
    return render(request,'mainapp/index.html', {'liste':liste})

@user_passes_test(lambda user:user.is_superuser)
def units(request):
    msg="Kayıt Giriniz."
    if request.method == 'POST':
        formset = UnitForm(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()
            msg="Kayıt başarılı."
            #return HttpResponseRedirect('')
            formset=UnitForm()
            # do something.
    else:
        formset=UnitForm()
    return render(request,'mainapp/formset.html',{'formset':formset, 'msg':msg})

@login_required
def addbook(request):
    msg="Kayıt Giriniz."
    if request.method=="POST":
        search=request.POST.get("search_text")
        #kitap kayıtlarda varsa;
        book_list=Book.objects.filter(isbn=search)
        if book_list:
            redirect("books/"+book_list[0].isbn)
        else:
            if request.method == 'POST':
                formset = BookForm(request.POST, request.FILES)
                if formset.is_valid():
                    formset.save()
                    msg="Kayıt başarılı."
                    #return HttpResponseRedirect('')
                    formset=BookForm()
                    # do something.
    else:
        formset=BookForm()
    return render(request,'mainapp/addbook.html',{'formset':formset, 'title':'Kitap Ekle', 'msg':msg})

@user_passes_test(lambda user:user.is_superuser)
def libraries(request):
    msg="Kayıt Giriniz."
    if request.method == 'POST':
        formset = LibraryForm(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()
            msg="Kayıt başarılı."
            #return HttpResponseRedirect('')
            formset=LibraryForm()
            # do something.
    else:
        formset=LibraryForm()
    return render(request,'mainapp/formset.html',{'formset':formset,'title':'libraries', 'msg':msg})

@login_required
def readers(request):
    msg="Kayıt Giriniz."
    if request.method == 'POST':
        formset = ReaderForm(request.POST, request.FILES)
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
                reader.unit=(Unit.objects.filter(id=unit_id))[0]
                reader.id=id
                reader.save()

    else:
        formset=ReaderForm()
    return render(request,'mainapp/formset.html',{'formset':formset,'title':'readers', 'msg':msg})



@login_required
def lendings(request):
    if request.method=="POST":
        search=request.POST.get("search_text")
        liste=Book.objects.filter(title__contains=search)
    else:
        liste=Book.objects.all()
    return render(request,'mainapp/lending.html', {'liste':liste})


@login_required
def the_book(request,isbn):
    if request.method=="POST":
        book=Book.objects.filter(isbn=isbn)
        book.delete()
        return redirect("/index")
    else:
        book=Book.objects.filter(isbn=isbn)
    return render(request,'mainapp/book.html', {'book':book})



def login(request):
    return render(request,'mainapp/login.html')

@user_passes_test(lambda user:user.is_staff )
def users(request):
    if request.method == 'POST':
        formset = UserForm(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()
            #return HttpResponseRedirect('')
            formset=UserForm()
            # do something.
    else:
        formset=UserForm()
    return render(request,'mainapp/formset.html',{'formset':formset,'title':'users'})
