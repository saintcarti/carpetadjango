from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm
from django.contrib.auth.models import Group
from django.shortcuts import render





# Create your views here.
def indexView(request):
    return render(request,"home/index.html")



def loginView(request):
    if request.method == 'POST':
        usuario = request.POST.get('username')
        clave = request.POST.get('password')

        user = authenticate(request, username=usuario, password=clave)

        if user is not None:
            login(request, user)

            # Redirección según el grupo del usuario
            if user.groups.filter(name='admin').exists():
                return redirect('admin_dashboard')
            elif user.groups.filter(name='supervisor').exists():
                return redirect('supervisor_dashboard')
            elif user.groups.filter(name='vendedor').exists():
                return redirect('vendedor_dashboard')
            else:
                return render(request, 'acceso/login.html', {'error': 'No tienes permisos para ingresar'})
        else:
            return render(request, 'acceso/login.html', {'error': 'Usuario o contraseña incorrectos'})
    return render(request, 'acceso/login.html')


@login_required
@group_required('admin')
def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Guardar el usuario y asignar el grupo  # Iniciar sesión automáticamente después de registrarse
            return redirect('admin_dashboard')  # Redirigir a la página principal o a un dashboard
    else:
        form = CustomUserCreationForm()

    return render(request, 'dashboard/GestionUs/register.html', {'form': form})


def gestionarInformes(request):
    return render(request, "dashboard/GestionInfor/gestion_informes.html")


def logoutView(request):
    logout(request)
    return redirect('login')

from django.contrib.auth.decorators import login_required

@login_required
def baseView(request):
    # Verificar si el usuario pertenece a los grupos correspondientes
    is_admin = request.user.groups.filter(name='Administrador').exists()
    is_supervisor = request.user.groups.filter(name='Supervisor').exists()
    is_vendedor = request.user.groups.filter(name='Vendedor').exists()

    # Para depuración, puedes imprimir estas variables o pasarlas al contexto
    print(f"Is Admin: {is_admin}, Is Supervisor: {is_supervisor}, Is Vendedor: {is_vendedor}")

    return render(request, 'base.html', {
        'is_admin': is_admin,
        'is_supervisor': is_supervisor,
        'is_vendedor': is_vendedor,
    })



def dashboardView(request):

    tareas = Tarea.objects.all()
    context = {
        'tareas':tareas
    }
    
    return render(request, "dashboard/admin_dashboard.html",context)

def solicitud_view(request):
    # Obtener los datos necesarios para los selects
    clientes = Cliente.objects.all()
    productos_lista = productos.objects.all()
    vendedores = UserProfile.objects.all()

    context = {
        'clientes': clientes,
        'productos_lista': productos_lista,
        'vendedores': vendedores,
    }

    return render(request, 'dashboard/GestionInfor/gestion_reporte.html', context)


def supervisorView(request):
    return render(request, "dashboard/supervisor_dashboard.html")

def GestionUsuarioView(request):
    return render(request, "dashboard/GestionUs/gestion_usuario.html")

def blankView(request):
    return render(request, "dashboard/blank.html")

def vendedorView(request):
    return render(request, "dashboard/vendedor_dashboard.html")

##gestion de usuarios

def gestionUs(request):
    return render(request, "dashboard/GestionUs/gestion_usuario.html")

def detailView(request):
    return render(request, "dashboard/GestionUs/crud/detail.html")

def modifyUser(request):
    return render(request, "dashboard/GestionUs/crud/modify_user.html")

def createUser(request):
    return render(request, "dashboard/GestionUs/crud/create_user.html")

##gestion de productos

def gestionProd(request):
    return render(request, "dashboard/GestionProd/gestion_productos.html")

def createProd(request):
    return render(request, "dashboard/GestionProd/crud/create_product.html")

def modifyProd(request):
    return render(request, "dashboard/GestionProd/crud/modify_product.html")

def detailProd(request):
    return render(request, "dashboard/GestionProd/crud/detail.html")

def gestionCategoria(request):
    return render(request, "dashboard/GestionProd/gestionar_categorias.html")

def gestionReporte(request):
    return render(request, "dashboard/GestionInfor/gestion_reporte.html")

##gestion de tareas
def gestionTask(request):
    return render(request, "dashboard/GestionTareas/gestion_task.html")

def createTask(request):
    return render(request, "dashboard/GestionTareas/crud/create_task.html")

def modifyTask(request):
    return render(request, "dashboard/GestionTareas/crud/modify_task.html")

def detailTask(request):
    return render(request, "dashboard/GestionTareas/crud/detail.html")