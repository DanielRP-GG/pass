from rest_framework import serializers
from .models import Autor, Libro, Prestamo


class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = '__all__'

    def validate_identificacion(self, value):
        if not value.strip():
            raise serializers.ValidationError("La identificacion es obligatoria")
        return value.strip()

    def validate_nombre(self, value):
        if not value.strip():
            raise serializers.ValidationError("El nombre es obligatorio")
        return value.strip()


class LibroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Libro
        fields = '__all__'

    def validate_titulo(self, value):
        if not value.strip():
            raise serializers.ValidationError("El titulo es obligatorio")
        return value.strip()

    def validate_precio_alquiler(self, value):
        if value <= 0:
            raise serializers.ValidationError("El precio de alquiler debe ser mayor a 0")
        return value


class PrestamoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prestamo
        fields = '__all__'

    def validate_socio_nombre(self, value):
        if not value.strip():
            raise serializers.ValidationError("El nombre del socio es obligatorio")
        return value.strip()

    def validate_dias_prestamo(self, value):
        if value <= 0:
            raise serializers.ValidationError("Los dias de prestamo deben ser mayores a 0")
        return value

    def validate_costo_total(self, value):
        if value < 0:
            raise serializers.ValidationError("El costo total no puede ser negativo")
        return value
