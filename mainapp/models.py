from django.db import models
from django.db.models import UniqueConstraint, Q
from django.contrib.auth.models import User


class Unit(models.Model):
    id=models.CharField(max_length=8, primary_key=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    address=models.CharField(max_length=200)
    #user=models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.name+" - "+self.address

class Book(models.Model):
    isbn=models.CharField(verbose_name="isbn",max_length=13, primary_key=True)
    title=models.CharField(verbose_name="kitap adı",max_length=50)
    writer=models.CharField(verbose_name="yazar",max_length=50 )
    genre=models.CharField(verbose_name="tür",max_length=20)
    publisher=models.CharField(verbose_name="yayıncı",max_length=20)
    publish_year=models.IntegerField(verbose_name="yayın yılı",)
    pages=models.IntegerField(blank=True, verbose_name="Sayfa Sayısı")
    def __str__(self):
        return self.isbn +"-"+self.title

class Library(models.Model):
    unit=models.ForeignKey(Unit, on_delete=models.CASCADE)
    book=models.ForeignKey(Book,on_delete=models.CASCADE)
    amount=models.IntegerField(default=1)
    on_lending=models.IntegerField(default=0)
    description=models.CharField(max_length=100, default="")

    def __str__(self):
        return self.unit.__str__() +" - "+self.book.__str__()


class Reader(models.Model):
    unit=models.ForeignKey(Unit, on_delete=models.CASCADE)
    school_num=models.CharField(max_length=10, verbose_name="Okul Numarası")
    id=models.CharField(max_length=20, primary_key=True)
    name=models.CharField(max_length=50, verbose_name="İsim")
    grade=models.IntegerField(verbose_name='Sınıf')
    department=models.CharField(max_length=5,verbose_name="Şube")
    books_lended=models.IntegerField(default=1)
    books_on=models.IntegerField(default=1)
    def __str__(self):
        return str(self.grade)+"/"+self.department+" - "+self.school_num +" "+self.name


class Lending(models.Model):
    unit=models.ForeignKey(Unit, on_delete=models.CASCADE)
    library_entry=models.ForeignKey(Library, on_delete=models.CASCADE)
    reader=models.ForeignKey(Reader, on_delete=models.CASCADE)
    lend_date=models.DateField()
    back_date=models.DateField()
    returned=models.BooleanField(default=False)

    def __str__(self):
        return self.reader.__str__() +"-"+self.library_entry.book.__str__()
