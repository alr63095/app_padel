from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistroForm, ReservaForm
from .models import Club, Pista, Reserva
from django.http import JsonResponse

# Create your views here.
from django.http import HttpResponse


def home(request):
    return render(request, 'app_padel/home.html')


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
                return render(request, 'app_padel/login.html', {'error': "Usuario o Contraseña incorrectos"})
    return render(request, 'app_padel/login.html')


@login_required
def inicio(request):
    vars = {}
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inicio')
    if 'username' in request.POST:
        if request.POST['username']:
            vars['username'] = request.POST['username']
        else:
            return login_app
    clubs = Club.objects.all()
    vars['clubs'] = clubs
    form = ReservaForm()
    vars['form'] = form
    return render(request, 'app_padel/inicio.html', vars)


def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Registro exitoso! Por favor, inicia sesión.')
            return redirect('login')
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
            return redirect('inicio')
    else:
        form = ReservaForm()
    return render(request, 'app_padel/nuevaReserva.html', {'form': form})


def obtener_numero_pistas(request):
    if request.method == 'GET' and 'club_id' in request.GET:
        club_id = request.GET['club_id']
        club_id_n = int(club_id)
        if club_id_n > 0:
            numero_pistas = Pista.objects.filter(club_id=club_id).count()
            return JsonResponse({'numero_pistas': numero_pistas})
    else:
        return JsonResponse({'error': 'No se proporcionó el ID del club'})


def misReservas(request):
    # Obtener todas las reservas del usuario actual
    reservas = Reserva.objects.filter(usuario=request.user)
    return render(request, 'app_padel/misReservas.html', {'reservas': reservas})


def actualizarReserva(request, reserva_id):
    # Obtener la reserva a actualizar
    reserva = Reserva.objects.get(id=reserva_id)

    if request.method == 'POST':
        # Crear un formulario de reserva con los datos de la reserva existente y los datos proporcionados en el formulario
        form = ReservaForm(request.POST, instance=reserva)
        if form.is_valid():
            # Guardar los cambios en la reserva
            form.save()
            return redirect('misReservas')  # Redireccionar a la vista de misReservas
    else:
        # Crear un formulario de reserva con los datos de la reserva existente
        form = ReservaForm(instance=reserva)

    return render(request, 'app_padel/actualizar_reserva.html', {'form': form})


def delete_reserva(request, reserva_id):
    # Obtener la reserva a eliminar
    reserva = get_object_or_404(Reserva, pk=reserva_id)

    # Cambiar el valor de 'activo' a False
    reserva.activo = False
    reserva.save()
    return redirect('inicio')
