from django.db import models


class Autor(models.Model):
    identificacion = models.CharField(max_length=30, unique=True)
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=30, blank=True)
    email = models.EmailField(max_length=254, blank=True)

    def __str__(self):
        return self.nombre


class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    isbn = models.CharField(max_length=30, unique=True)
    categoria = models.CharField(max_length=80)
    precio_alquiler = models.DecimalField(max_digits=8, decimal_places=2)
    disponible = models.BooleanField(default=True)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, related_name='libros')

    def __str__(self):
        return self.titulo


class Prestamo(models.Model):
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, related_name='prestamos')
    socio_nombre = models.CharField(max_length=100)
    fecha_prestamo = models.DateTimeField(auto_now_add=True)
    dias_prestamo = models.IntegerField()
    costo_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Prestamo: {self.libro.titulo} a {self.socio_nombre}"
