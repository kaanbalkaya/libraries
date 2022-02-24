from django.db import models
from django.db.models import UniqueConstraint, Q
from django.contrib.auth.models import User


# Create your models here.
class Unit(models.Model):
    id=models.CharField(max_length=8, primary_key=True)
    name=models.CharField(max_length=100)
    address=models.CharField(max_length=200)
    #user=models.OneToOneField(User, on_delete=models.CASCADE)

class Book(models.Model):
    isbn=models.CharField(db_column="isbn", verbose_name="isbn",max_length=13, primary_key=True)
    title=models.CharField(db_column="title", verbose_name="kitap adı",max_length=50)
    writer=models.CharField(db_column="writer", verbose_name="yazar",max_length=50 )
    genre=models.CharField(db_column="genre", verbose_name="tür",max_length=20)
    publisher=models.CharField(db_column="publisher", verbose_name="yayıncı",max_length=20)
    publish_year=models.IntegerField(db_column="publish_year", verbose_name="yayın yılı",)

class Library(models.Model):
    unit=models.ForeignKey(Unit, on_delete=models.CASCADE)
    book=models.ForeignKey(Book,on_delete=models.CASCADE)
    amount=models.IntegerField(default=1)
    description=models.CharField(max_length=100, default="")
    class Meta:
        UniqueConstraint(fields=["unit","book"], name="book_record")

class Reader(models.Model):
    unit=models.ForeignKey(Unit, on_delete=models.CASCADE)
    school_num=models.CharField(max_length=10, verbose_name="Okul Numarası")
    id=models.CharField(max_length=20, primary_key=True)
    name=models.CharField(max_length=50)
    grade=models.IntegerField()
    department=models.CharField(max_length=5)
    books_lended=models.IntegerField(default=0)
    #class Meta:
    #    constraints = [UniqueConstraint(fields=['unit', 'school_num'], name='reader_id'),]

class Lending(models.Model):
    unit=models.ForeignKey(Unit, on_delete=models.CASCADE)
    reader=models.ForeignKey(Reader, on_delete=models.CASCADE)
    book=models.ForeignKey(Book,on_delete=models.CASCADE)
    lend_date=models.DateField()
    back_date=models.DateField()
