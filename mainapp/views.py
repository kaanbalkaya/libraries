from django.shortcuts import render
from django.http import HttpResponseRedirect
from .formsets import UnitForm, BookForm, LibraryForm, ReaderForm, LendingForm, UserForm
from .models import Book, Unit, Library, Reader, Lending
from django.contrib.auth.decorators import login_required, user_passes_test

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
def books(request):
    msg="Kayıt Giriniz."
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
    return render(request,'mainapp/formset.html',{'formset':formset, 'title':'books', 'msg':msg})

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
            formset.save()
            msg="Kayıt başarılı."
            #return HttpResponseRedirect('')
            formset=ReaderForm()
            # do something.
    else:
        formset=ReaderForm()
    return render(request,'mainapp/formset.html',{'formset':formset,'title':'readers', 'msg':msg})



@login_required
def lendings(request):
    msg="Kayıt Giriniz."
    if request.method == 'POST':
        formset = LendingForm(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()
            msg="Kayıt başarılı."
            #return HttpResponseRedirect('')
            formset=LendingForm()
            # do something.
    else:
        formset=LendingForm()
    return render(request,'mainapp/formset.html',{'formset':formset, 'title':'lendings', 'msg':msg})


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
