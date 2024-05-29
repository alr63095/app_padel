from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistroForm, ReservaForm,DetallesClubForm
from .models import Club, Pista, Reserva , DetallesClub , Dimensiones
from django.http import JsonResponse,HttpResponse
from .funciones import convert_base64_to_image,convert_image_to_base64
from django.utils import timezone
from datetime import datetime, timedelta

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
    user = request.user
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
    vars['user'] = user
    clubs = Club.objects.all()
    club = Club.objects.filter(admin_id_id=user.id)
    if club.exists():
        vars['club'] = club[0]
    else:
        vars['club'] = False
    vars['clubs'] = clubs
    form = ReservaForm()
    vars['form'] = form
    return render(request, 'app_padel/inicio.html', vars)

@login_required
def usuario(request):
    usuario_actual = request.user
    context = {
        'usuario': usuario_actual,
    }
    return render(request, 'app_padel/usuario.html', context)


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


def crear_reserva_antiguo(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirigir a alguna página después de crear la reserva (por ejemplo, la página de inicio)
            return redirect('inicio')
    else:
        vars = {}
        user = request.user
        vars['user'] = user
        clubs = Club.objects.all()
        club = Club.objects.filter(admin_id_id=user.id)
        if club.exists():
            vars['club'] = club[0]
        else:
            vars['club'] = False
        vars['clubs'] = clubs
        form = ReservaForm()
        vars['form'] = form
    return render(request, 'app_padel/nuevaReserva.html', {'vars': vars})

def crear_reserva(request):
    #horas = [f"{hour:02d}:00" for hour in range(8, 23)] + [f"{hour:02d}:30" for hour in range(8, 22)]
    horas_dim = Dimensiones.objects.all()
    horas_list = horas_dim.values_list('horas_disponibles', flat=True).order_by('horas_disponibles')
    horas = []
    for h in horas_list:
        horas.append(h)
    horas.sort()
    ciudades = Club.objects.values('direccion').distinct()
    hoy = timezone.now().date().isoformat()
    if request.method == "POST":
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')
        ciudad = request.POST.get('ciudad', '')

        if not fecha or not hora:
            return render(request, 'app_padel/nuevaReserva.html', {'horas': horas ,'ciudades': ciudades, 'hoy' : hoy,'error': 'Debe seleccionar una fecha y una hora'})
        # Verificación del lado del servidor
        if fecha and timezone.datetime.strptime(fecha, '%Y-%m-%d').date() < timezone.now().date():
            return render(request, 'app_padel/nuevaReserva.html', {'horas': horas ,'ciudades': ciudades, 'hoy' : hoy,'error': 'Debe seleccionar una fecha igual o superior al dia de hoy'})

        fecha_hora = f"{fecha} {hora}"
        fecha_hora_dt = timezone.datetime.strptime(fecha_hora, '%Y-%m-%d %H:%M')

        # Filtrar reservas activas para la fecha y hora seleccionadas
        reservas = Reserva.objects.filter(hora_inicio=fecha_hora_dt, activo=True)

        # Obtener pistas no reservadas
        pistas_reservadas = reservas.values_list('pista_id', flat=True)
        pistas_disponibles = Pista.objects.exclude(id__in=pistas_reservadas)

        if ciudad:
            clubs = Club.objects.filter(direccion__icontains=ciudad, pistas__in=pistas_disponibles).distinct()
        else:
            clubs = Club.objects.filter(pistas__in=pistas_disponibles).distinct()

        return render(request, 'app_padel/nuevaReserva.html', {
            'horas': horas,
            'clubs': clubs,
            'fecha': fecha,
            'hora': hora,
            'ciudad': ciudad,
            'ciudades': ciudades, 
            'hoy' : hoy
        })

    return render(request, 'app_padel/nuevaReserva.html', {'horas': horas ,'ciudades': ciudades, 'hoy' : hoy})

def reserva_pista(request, pista_id):
    pista = get_object_or_404(Pista, id=pista_id)

    if request.method == 'POST':
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')
        fecha_hora = f"{fecha} {hora}"
        fecha_hora_dt = timezone.datetime.strptime(fecha_hora, '%Y-%m-%d %H:%M')
        hora_fin =  fecha_hora_dt + timedelta(minutes=90)
        # Crear la reserva
        Reserva.objects.create(
            pista=pista,
            usuario=request.user,
            hora_inicio=fecha_hora_dt,
            hora_fin = hora_fin,
            created = datetime.now(),
            activo=True
        )
        return redirect('misReservas')
    fecha = request.GET.get('fecha')
    hora = request.GET.get('hora')
    return render(request, 'app_padel/reservaPista.html', {'pista': pista ,'fecha': fecha, 'hora': hora })

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
    fecha_actual = datetime.now()
    reservas_activas = Reserva.objects.filter(usuario=request.user).filter(activo=True).filter(hora_inicio__gt=fecha_actual)
    reservas_historico = Reserva.objects.filter(usuario=request.user).filter(activo=True).filter(hora_inicio__lt=fecha_actual)
    return render(request, 'app_padel/misReservas.html', {'reservas_activas': reservas_activas,'reservas_historico': reservas_historico})


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
    return misReservas(request)

def create_detalles_club(request):
    if request.method == 'POST':
        form = DetallesClubForm(request.POST, request.FILES)
        if form.is_valid():
            detalles_club = form.save(commit=False)
            if 'imagen_principal' in request.FILES:
                detalles_club.imagen_principal = convert_image_to_base64(request.FILES['imagen_principal'])
            if 'imagen_secundaria' in request.FILES:
                detalles_club.imagen_secundaria = convert_image_to_base64(request.FILES['imagen_secundaria'])
            detalles_club.save()
            return redirect('inicio')
    else:
        form = DetallesClubForm()
    return render(request, 'app_padel/detalles_club_form.html', {'form': form})

def clubs_disponibles(request):
    clubs = Club.objects.all()
    ciudades = {}

    for club in clubs:
        ciudad = club.direccion.split(',')[-1].strip()
        if ciudad not in ciudades:
            ciudades[ciudad] = []
        ciudades[ciudad].append(club)

    context = {
        'ciudades': ciudades,
        'clubs': clubs
    }
    return render(request, 'app_padel/clubsDisponibles.html', context)