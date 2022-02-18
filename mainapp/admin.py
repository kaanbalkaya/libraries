from django.contrib import admin
from .models import Unit, Book, Library, Reader,Lending
# Register your models here.

admin.site.register(Unit)
admin.site.register(Book)
admin.site.register(Library)
admin.site.register(Reader)
admin.site.register(Lending)
