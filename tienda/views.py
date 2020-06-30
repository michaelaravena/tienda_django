# from django.http import HttpResponse
from pyexpat.errors import messages

from django.contrib import messages  # envia mensajes del servidor al cliente
from django.contrib.auth import authenticate  # permite revisar si un usuario existe
from django.contrib.auth import login  # se encarga de crear la sesión
from django.contrib.auth import logout  # se encarga de cerrar la sesión
from django.shortcuts import redirect
from django.shortcuts import render  # permite responder al cliente mostrando un templatepreviamente renderizado
from django.contrib.auth.models import User  # esta clase permite dar de alta nuevos usuarios
from .forms import RegisterForm


def index(request):
    return render(request, 'index.html', {
        'message': 'Listado de productos',
        'title': 'Productos',
        'products': [
            {'title': 'polera', 'price': 1000, 'stock': True},
            {'title': 'camisa', 'price': 2000, 'stock': False},
            {'title': 'pantalon', 'price': 5000, 'stock': True}
        ]
    })  # recibe 3 argumentos, siendo el ultimo un diccionario


def login_view(request):

    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST.get('username')  # diccionario
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)  # si no existe retorna NONE

        if user:
            login(request, user)  # acá se crea la sesión con el usuario
            messages.success(request, 'Bienvenido {}'.format(user.username))
            return redirect('index')
        else:
            messages.error(request, 'Usuario o contraseña no validos')

    return render(request, 'users/login.html', {})


def logout_view(request):
    logout(request)
    messages.success(request, 'Sesión cerrada exitosamente')
    return redirect('login')


def register_view(request):

    if request.user.is_authenticated:
        return redirect('index')

    form = RegisterForm(request.POST or None)  # si la peticion es por POST genera formulario con datos del cliente
    if request.method == 'POST' and form.is_valid():

        user = form.save()
        if user:
            login(request,user)
            messages.success(request, 'Usuario creado exitosamente')
            return redirect('index')

    return render(request, 'users/register.html', {
        'form': form
    })
