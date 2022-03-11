from django.forms import ModelForm
from .models import Unit, Book, Library, Reader, Lending
from django.contrib.auth.models import User

class UnitForm(ModelForm):
    class Meta:
        model=Unit
        fields=['id','name','address']

class BookForm(ModelForm):
    class Meta:
        model=Book
        fields='__all__'

class LibraryForm(ModelForm):
    class Meta:
        model=Library
        fields=['book','amount']

class ReaderForm(ModelForm):
    class Meta:
        model=Reader
        fields=['name','grade','department']

class LendingForm(ModelForm):
    class Meta:
        model=Lending
        fields='__all__'

class UserForm(ModelForm):
        class Meta:
            model=User
            fields=['username', 'password']
