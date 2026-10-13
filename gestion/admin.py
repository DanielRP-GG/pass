from django.contrib import admin
from .models import Autor, Libro, Prestamo


class LibroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'precio_alquiler', 'disponible', 'autor')


admin.site.register(Autor)
admin.site.register(Libro, LibroAdmin)
admin.site.register(Prestamo)
