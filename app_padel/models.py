from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Club(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    activo = models.BooleanField(default=1)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    # Otros campos para la información del club

    def __str__(self):
        return self.nombre

class Pista(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    numero = models.IntegerField()
    descripcion = models.CharField(max_length=100,default="")
    activo = models.BooleanField(default=1)
    # Otros campos para la información de la pista

    def __str__(self):
        return f"Pista {self.descripcion} - {self.club.nombre}"

class Reserva(models.Model):
    pista = models.ForeignKey(Pista, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    hora_inicio = models.DateTimeField()
    hora_fin = models.DateTimeField()
    updated = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField()
    activo = models.BooleanField(default=1)

    def __str__(self):
        return f"Reserva de {self.usuario.username} en {self.pista} de {self.hora_inicio} a {self.hora_fin}" 
    
class Dimensiones(models.Model):
    horas_disponibles = models.CharField(max_length=50)
