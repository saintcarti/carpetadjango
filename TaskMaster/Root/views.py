from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm
from django.contrib.auth.models import Group,User
from django.shortcuts import render
from .forms import SolicitudForm, DetalleSolicitudForm
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from django.shortcuts import render
from .models import Solicitud 





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
def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Guardar el usuario y asignar el grupo  # Iniciar sesión automáticamente después de registrarse
            return redirect('admin_dashboard')  # Redirigir a la página principal o a un dashboard
    else:
        form = CustomUserCreationForm()

    return render(request, 'dashboard/GestionUs/register.html', {'form': form})

@login_required
def gestionarInformes(request):
    if request.method == 'POST':
        solicitud_form = SolicitudForm(request.POST)
        detalle_form = DetalleSolicitudForm(request.POST)
        if solicitud_form.is_valid() and detalle_form.is_valid():
            solicitud = solicitud_form.save()  # Crea la solicitud
            detalle = detalle_form.save(commit=False)
            detalle.solicitud = solicitud  # Asocia la solicitud al detalle
            detalle.save()  # Guarda el detalle
            return redirect('lista_solicitudes')  # Redirige a una vista de lista
    else:
        solicitud_form = SolicitudForm()
        detalle_form = DetalleSolicitudForm()

    user_groups = request.user.groups.values_list('name', flat=True)
    print(user_groups)
    # Verificar si el usuario pertenece a los grupos específicos
    is_admin = 'admin' in user_groups
    is_supervisor = 'supervisor' in user_groups
    is_vendedor = 'vendedor' in user_groups

    # Para depuración, puedes imprimir estas variables o pasarlas al contexto
    print(f"Is Admin: {is_admin}, Is Supervisor: {is_supervisor}, Is Vendedor: {is_vendedor}")

    # Crear el contexto con las variables necesarias
    context = {
        'is_admin': is_admin,
        'is_supervisor': is_supervisor,
        'is_vendedor': is_vendedor,
        'solicitud_form': solicitud_form,
        'detalle_form': detalle_form
    }



    return render(request, "dashboard/GestionInfor/gestion_informes.html",context)

def generar_pdf(request):
    # Creamos un objeto en memoria para el PDF
    buffer = BytesIO()

    # Creamos un canvas ReportLab
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Añadimos un título o contenido al PDF
    p.drawString(100, height - 100, "Listado de Solicitudes")
    
    y_position = height - 150
    solicitudes = Solicitud.objects.all()  # Obtener todas las solicitudes desde la base de datos
    
    for soli in solicitudes:
        p.drawString(100, y_position, f"Solicitud: {soli}")  # Agregar datos de la solicitud al PDF
        y_position -= 20
    
    # Finalizamos el PDF
    p.showPage()
    p.save()

    # Volvemos al principio del buffer para que el archivo sea leído
    buffer.seek(0)

    # Devolvemos el PDF como respuesta HTTP
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="solicitudes.pdf"'
    return response

@login_required
def lista_solicitudes(request):
    solicitudes = Solicitud.objects.all()
    user_groups = request.user.groups.values_list('name', flat=True)
    print(user_groups)
    # Verificar si el usuario pertenece a los grupos específicos
    is_admin = 'admin' in user_groups
    is_supervisor = 'supervisor' in user_groups
    is_vendedor = 'vendedor' in user_groups

    # Para depuración, puedes imprimir estas variables o pasarlas al contexto
    print(f"Is Admin: {is_admin}, Is Supervisor: {is_supervisor}, Is Vendedor: {is_vendedor}")

    # Crear el contexto con las variables necesarias
    context = {
        'is_admin': is_admin,
        'is_supervisor': is_supervisor,
        'is_vendedor': is_vendedor,
        'solicitudes': solicitudes
    }
    return render(request, 'dashboard/GestionInfor/lista_solicitudes.html', context)

def logoutView(request):
    logout(request)
    return redirect('login')


@login_required
def baseView(request):
    # Obtener los nombres de los grupos del usuario logueado
    user_groups = request.user.groups.values_list('name', flat=True)
    print(user_groups)
    # Verificar si el usuario pertenece a los grupos específicos
    is_admin = 'admin' in user_groups
    is_supervisor = 'supervisor' in user_groups
    is_vendedor = 'vendedor' in user_groups

    # Para depuración, puedes imprimir estas variables o pasarlas al contexto
    print(f"Is Admin: {is_admin}, Is Supervisor: {is_supervisor}, Is Vendedor: {is_vendedor}")

    # Crear el contexto con las variables necesarias
    context = {
        'is_admin': is_admin,
        'is_supervisor': is_supervisor,
        'is_vendedor': is_vendedor
    }

    return render(request, 'base.html', context)



@login_required
def dashboardView(request):

    user_groups = request.user.groups.values_list('name', flat=True)
    print(user_groups)
    # Verificar si el usuario pertenece a los grupos específicos
    is_admin = 'admin' in user_groups
    is_supervisor = 'supervisor' in user_groups
    is_vendedor = 'vendedor' in user_groups

    # Para depuración, puedes imprimir estas variables o pasarlas al contexto
    print(f"Is Admin: {is_admin}, Is Supervisor: {is_supervisor}, Is Vendedor: {is_vendedor}")

    # Crear el contexto con las variables necesarias
    context = {
        'is_admin': is_admin,
        'is_supervisor': is_supervisor,
        'is_vendedor': is_vendedor
    }
    return render(request, "dashboard/admin_dashboard.html",context)

@login_required
def solicitud_view(request):
    clientes = Cliente.objects.all()
    productos_lista = productos.objects.all()
    vendedores = UserProfile.objects.filter(role='vendedor')
    user_groups = request.user.groups.values_list('name', flat=True)
    print(user_groups)
    # Verificar si el usuario pertenece a los grupos específicos
    is_admin = 'admin' in user_groups
    is_supervisor = 'supervisor' in user_groups
    is_vendedor = 'vendedor' in user_groups

    # Para depuración, puedes imprimir estas variables o pasarlas al contexto
    print(f"Is Admin: {is_admin}, Is Supervisor: {is_supervisor}, Is Vendedor: {is_vendedor}")

    # Crear el contexto con las variables necesarias
    context = {
        'is_admin': is_admin,
        'is_supervisor': is_supervisor,
        'is_vendedor': is_vendedor,
        'clientes': clientes,
        'productos_lista': productos_lista,
        'vendedores': vendedores,
    }   

    return render(request, 'dashboard/GestionInfor/gestion_reporte.html', context)

@login_required
def supervisorView(request):
    user_groups = request.user.groups.values_list('name', flat=True)
    print(user_groups)
    # Verificar si el usuario pertenece a los grupos específicos
    is_admin = 'admin' in user_groups
    is_supervisor = 'supervisor' in user_groups
    is_vendedor = 'vendedor' in user_groups

    # Para depuración, puedes imprimir estas variables o pasarlas al contexto
    print(f"Is Admin: {is_admin}, Is Supervisor: {is_supervisor}, Is Vendedor: {is_vendedor}")

    # Crear el contexto con las variables necesarias
    context = {
        'is_admin': is_admin,
        'is_supervisor': is_supervisor,
        'is_vendedor': is_vendedor
    }
    return render(request, "dashboard/supervisor_dashboard.html",context)

@login_required
def GestionUsuarioView(request):
    usuarios = User.objects.all()  # Obtener todos los usuarios
    user_groups = request.user.groups.values_list('name', flat=True)  # Obtener los grupos del usuario
    print("User groups:", list(user_groups))  # Verificar qué grupos tiene el usuario
    
    # Verificar si el usuario pertenece a los grupos específicos
    is_admin = 'admin' in user_groups
    is_supervisor = 'supervisor' in user_groups
    is_vendedor = 'vendedor' in user_groups

    # Para depuración, puedes imprimir estas variables
    print(f"Is Admin: {is_admin}, Is Supervisor: {is_supervisor}, Is Vendedor: {is_vendedor}")

    # Crear el contexto con las variables necesarias
    context = {
        'is_admin': is_admin,
        'is_supervisor': is_supervisor,
        'is_vendedor': is_vendedor,
        'usuario': usuarios
    }

    return render(request, "dashboard/GestionUs/gestion_usuario.html", context)



@login_required
def vendedorView(request):
    user_groups = request.user.groups.values_list('name', flat=True)
    print(user_groups)
    # Verificar si el usuario pertenece a los grupos específicos
    is_admin = 'admin' in user_groups
    is_supervisor = 'supervisor' in user_groups
    is_vendedor = 'vendedor' in user_groups

    # Para depuración, puedes imprimir estas variables o pasarlas al contexto
    print(f"Is Admin: {is_admin}, Is Supervisor: {is_supervisor}, Is Vendedor: {is_vendedor}")

    # Crear el contexto con las variables necesarias
    context = {
        'is_admin': is_admin,
        'is_supervisor': is_supervisor,
        'is_vendedor': is_vendedor
    }
    return render(request, "dashboard/vendedor_dashboard.html",context)

##gestion de usuarios

def detailView(request):
    return render(request, "dashboard/GestionUs/crud/detail.html")

def modifyUser(request):
    return render(request, "dashboard/GestionUs/crud/modify_user.html")

def createUser(request):
    return render(request, "dashboard/GestionUs/crud/create_user.html")

##gestion de productos
@login_required
def gestionProd(request):
    user_groups = request.user.groups.values_list('name', flat=True)
    print(user_groups)
    # Verificar si el usuario pertenece a los grupos específicos
    is_admin = 'admin' in user_groups
    is_supervisor = 'supervisor' in user_groups
    is_vendedor = 'vendedor' in user_groups

    # Para depuración, puedes imprimir estas variables o pasarlas al contexto
    print(f"Is Admin: {is_admin}, Is Supervisor: {is_supervisor}, Is Vendedor: {is_vendedor}")

    # Crear el contexto con las variables necesarias
    context = {
        'is_admin': is_admin,
        'is_supervisor': is_supervisor,
        'is_vendedor': is_vendedor
    }
    return render(request, "dashboard/GestionProd/gestion_productos.html",context)

def createProd(request):
    return render(request, "dashboard/GestionProd/crud/create_product.html")

def modifyProd(request):
    return render(request, "dashboard/GestionProd/crud/modify_product.html")

def detailProd(request):
    return render(request, "dashboard/GestionProd/crud/detail.html")




def gestionReporte(request):
    user_groups = request.user.groups.values_list('name', flat=True)
    print(user_groups)
    # Verificar si el usuario pertenece a los grupos específicos
    is_admin = 'admin' in user_groups
    is_supervisor = 'supervisor' in user_groups
    is_vendedor = 'vendedor' in user_groups

    # Para depuración, puedes imprimir estas variables o pasarlas al contexto
    print(f"Is Admin: {is_admin}, Is Supervisor: {is_supervisor}, Is Vendedor: {is_vendedor}")

    # Crear el contexto con las variables necesarias
    context = {
        'is_admin': is_admin,
        'is_supervisor': is_supervisor,
        'is_vendedor': is_vendedor
    }   
    return render(request, "dashboard/GestionInfor/gestion_reporte.html",context)

##gestion de tareas
def gestionTask(request):
    user_groups = request.user.groups.values_list('name', flat=True)
    print(user_groups)
    # Verificar si el usuario pertenece a los grupos específicos
    is_admin = 'admin' in user_groups
    is_supervisor = 'supervisor' in user_groups
    is_vendedor = 'vendedor' in user_groups

    # Para depuración, puedes imprimir estas variables o pasarlas al contexto
    print(f"Is Admin: {is_admin}, Is Supervisor: {is_supervisor}, Is Vendedor: {is_vendedor}")

    # Crear el contexto con las variables necesarias
    context = {
        'is_admin': is_admin,
        'is_supervisor': is_supervisor,
        'is_vendedor': is_vendedor
    }
    return render(request, "dashboard/GestionTareas/gestion_task.html",context)

def createTask(request):
    return render(request, "dashboard/GestionTareas/crud/create_task.html")

def modifyTask(request):
    return render(request, "dashboard/GestionTareas/crud/modify_task.html")

def detailTask(request):
    return render(request, "dashboard/GestionTareas/crud/detail.html")