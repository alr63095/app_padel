from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistroForm,ReservaForm
from .models import Club,Pista
from django.http import JsonResponse


# Create your views here.
from django.http import HttpResponse

def login_app(request):
    if request.method == 'POST':
        # Verifica si el campo 'username' está presente en el formulario
        if 'username' in request.POST:
            # Resto del código para autenticar al usuario, etc.
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirige al usuario a una página de inicio o a donde quieras después del inicio de sesión
                return redirect('inicio')
            else:
                # Si las credenciales son inválidas, muestra un mensaje de error
                messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
                return render(request, 'app_padel/login.html',{'error': "Usuario o Contraseña incorrectos"} )
    return render(request, 'app_padel/login.html')

@login_required
def inicio(request):
    vars = {}
    if 'username' in request.POST:
        if request.POST['username']:
            vars['username'] = request.POST['username']
        else:
            return login_app
    clubs = Club.objects.all()
    vars['clubs'] = clubs
    return render(request, 'app_padel/inicio.html',vars) 

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return inicio(request)
    else:
        form = RegistroForm()
    return render(request, 'app_padel/registro.html', {'form': form})

def logout_view(request):
    # Cierra la sesión del usuario
    logout(request)
    # Redirige a la página de inicio o a donde desees después del cierre de sesión
    return redirect('login')

def crear_reserva(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirigir a alguna página después de crear la reserva (por ejemplo, la página de inicio)
            return redirect('nombre_de_la_ruta')  # Reemplaza 'nombre_de_la_ruta' con el nombre de la ruta a la que deseas redirigir
    else:
        form = ReservaForm()
    return render(request, 'app_padel/nuevaReserva.html', {'form': form})

def obtener_numero_pistas(request):
    if request.method == 'GET' and 'club_id' in request.GET:
        club_id = request.GET['club_id']
        club_id_n = int(club_id)
        if club_id_n > 0 :   
            numero_pistas = Pista.objects.filter(club_id=club_id).count()
            return JsonResponse({'numero_pistas': numero_pistas})
    else:
        return JsonResponse({'error': 'No se proporcionó el ID del club'})