from django.forms import ModelForm
from .models import Unit, Book, Library, Reader, Lending
from django.contrib.auth.models import User

class UnitForm(ModelForm):
    class Meta:
        model=Unit
        fields='__all__'

class BookForm(ModelForm):
    class Meta:
        model=Book
        fields='__all__'

class LibraryForm(ModelForm):
    class Meta:
        model=Library
        fields='__all__'

class ReaderForm(ModelForm):
    class Meta:
        model=Reader
        fields='__all__'

class LendingForm(ModelForm):
    class Meta:
        model=Lending
        fields='__all__'

class UserForm(ModelForm):
        class Meta:
            model=User
            fields=['username', 'password']
