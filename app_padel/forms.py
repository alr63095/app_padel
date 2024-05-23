from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Reserva,DetallesClub

class RegistroForm(UserCreationForm):
    email = forms.EmailField(max_length=100)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class ReservaForm(ModelForm):
    class Meta:
        model = Reserva
        fields = ['pista', 'hora_inicio', 'usuario']


class DetallesClubForm(forms.ModelForm):
    class Meta:
        model = DetallesClub
        fields = ['ubicacion', 'descripcion_larga', 'numero_pistas', 'imagen_principal', 'imagen_secundaria']
        widgets = {
            'imagen_principal': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
            'imagen_secundaria': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
        }