from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm
from django.contrib.auth.models import Group,User
from django.shortcuts import render
from .forms import SolicitudForm, DetalleSolicitudForm,ProductoForm,TareaForm
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from django.shortcuts import render
from .models import Solicitud ,productos,Tarea





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

def generar_pdf(request, solicitud_id):
    # Buscar la solicitud correspondiente al ID
    try:
        solicitud = Solicitud.objects.get(idSolicitud=solicitud_id)
    except Solicitud.DoesNotExist:
        return HttpResponse("Solicitud no encontrada.", status=404)

    # Crear un buffer para generar el PDF
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Información de la solicitud
    p.drawString(100, height - 50, f"Informe de Solicitud #{solicitud.idSolicitud}")
    p.drawString(100, height - 70, f"Cliente: {solicitud.cliente.nombre}")
    p.drawString(100, height - 90, f"Vendedor: {solicitud.vendedor.user.username if solicitud.vendedor else 'N/A'}")
    p.drawString(100, height - 110, f"Fecha Solicitud: {solicitud.fechaSolicitud}")

    # Tabla de detalles de la solicitud
    y_position = height - 150
    p.drawString(100, y_position, "Detalles de la Solicitud:")
    y_position -= 20

    for detalle in solicitud.detallesolicitud_set.all():
        p.drawString(100, y_position, f"Producto: {detalle.producto.nombreProducto}")
        p.drawString(300, y_position, f"Cantidad: {detalle.cantidad}")
        p.drawString(450, y_position, f"Subtotal: ${detalle.subtotal():.2f}")
        y_position -= 20

    # Total
    y_position -= 20
    p.drawString(100, y_position, f"Total: ${solicitud.calcular_total():.2f}")

    # Finalizar el PDF
    p.showPage()
    p.save()

    # Devolver el PDF como respuesta
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="solicitud_{solicitud.idSolicitud}.pdf"'
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

    if is_admin:
        solicitudes = solicitudes
    elif is_supervisor:
    # Filtrar solicitudes asignadas a los vendedores supervisados
        solicitudes = solicitudes.filter(vendedor__role='vendedor')
    elif is_vendedor:
        solicitudes = solicitudes.filter(vendedor=request.user.userprofile)

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
def delete_solicitud(request, solicitud_id):
    try:
        solicitud = Solicitud.objects.get(idSolicitud=solicitud_id)
        solicitud.delete()
        messages.success(request, 'Solicitud eliminada correctamente.')
        return redirect('lista_solicitudes')
    except Solicitud.DoesNotExist:
        messages.error(request, 'La solicitud no existe.')
        return redirect('lista_solicitudes')


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
def eliminar_usuario(request,id):
    usuario = User.objects.get(id=id)
    usuario.delete()
    return redirect('gestion_usuario')



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


##gestion de productos
@login_required
def gestionProd(request):
    producto = productos.objects.all()
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
        'producto': producto
    }
    return render(request, "dashboard/GestionProd/gestion_productos.html",context)


@login_required
def createProd(request):
    user_groups = request.user.groups.values_list('name', flat=True)
    print(user_groups)
    # Verificar si el usuario pertenece a los grupos específicos
    is_admin = 'admin' in user_groups
    is_supervisor = 'supervisor' in user_groups
    is_vendedor = 'vendedor' in user_groups

    # Para depuración, puedes imprimir estas variables o pasarlas al contexto
    print(f"Is Admin: {is_admin}, Is Supervisor: {is_supervisor}, Is Vendedor: {is_vendedor}")

    # Crear el contexto con las variables necesarias
    

    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('gestion_productos')  # Cambia esto al nombre de la URL que prefieras
    else:
        form = ProductoForm()

    context = {
        'is_admin': is_admin,
        'is_supervisor': is_supervisor,
        'is_vendedor': is_vendedor,
        'form': form
    }
    return render(request, "dashboard/GestionProd/crud/create_product.html" ,context)


@login_required
def modifyProd(request, id):
    product = get_object_or_404(productos, idProducto=id)

    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado con éxito.")
            return redirect('gestion_productos')  # Redirigir a la página de gestión de productos
        else:
            messages.error(request, "Hubo un error al actualizar el producto.")
    else:
        form = ProductoForm(instance=product)

    user_groups = request.user.groups.values_list('name', flat=True)
    is_admin = 'admin' in user_groups
    is_supervisor = 'supervisor' in user_groups
    is_vendedor = 'vendedor' in user_groups

    context = {
        'is_admin': is_admin,
        'is_supervisor': is_supervisor,
        'is_vendedor': is_vendedor,
        'form': form,
    }

    return render(request, "dashboard/GestionProd/crud/modify_product.html", context)



def detailProd(request):
    

    return render(request, "dashboard/GestionProd/crud/detail.html")

def deleteProd(request, id):
    product = get_object_or_404(productos, idProducto = id)
    product.delete()
    return redirect('gestion_productos')




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
@login_required
def gestionTask(request):
    """
    Vista única para gestionar las tareas según el rol del usuario:
    - Admin: ve todas las tareas.
    - Supervisor: ve las tareas asignadas a los vendedores.
    - Vendedor: ve solo sus propias tareas.
    """
    user_groups = request.user.groups.values_list('name', flat=True)

    # Verificar si el usuario pertenece a los grupos específicos
    is_admin = 'admin' in user_groups
    is_supervisor = 'supervisor' in user_groups
    is_vendedor = 'vendedor' in user_groups

    # Filtrar las tareas según el rol del usuario
    if is_admin:
        tasks = Tarea.objects.all()  # Los admins ven todas las tareas
    elif is_supervisor:
        tasks = Tarea.objects.filter(usuario__role='vendedor')  # Supervisores ven tareas de vendedores
    elif is_vendedor:
        tasks = Tarea.objects.filter(usuario=request.user.userprofile)  # Vendedores ven sus propias tareas
    else:
        tasks = Tarea.objects.none()  # En caso de que el usuario no pertenezca a ningún rol definido

    # Crear el contexto con las variables necesarias
    context = {
        'tasks': tasks,
        'is_admin': is_admin,
        'is_supervisor': is_supervisor,
        'is_vendedor': is_vendedor,
    }

    return render(request, "dashboard/GestionTareas/gestion_task.html", context)

def createTask(request):

    if request.method == 'POST':
        form = TareaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gestion_task')  # Cambia 'gestion_tareas' al nombre de tu URL para listar tareas
    else:
        form = TareaForm()

    user_groups = request.user.groups.values_list('name', flat=True)

    is_admin = 'admin' in user_groups
    is_supervisor = 'supervisor' in user_groups
    is_vendedor = 'vendedor' in user_groups

    context = {
        'is_admin': is_admin,
        'is_supervisor': is_supervisor,
        'is_vendedor': is_vendedor,
        'form': form
    }


    return render(request, "dashboard/GestionTareas/crud/create_task.html",context)

def modifyTask(request, id):
    task = get_object_or_404(Tarea, idTarea=id)

    if request.method == "POST":
        form = TareaForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Tarea actualizada con éxito.")
            return redirect('gestion_task')
        else:
            messages.error(request, "Hubo un error al actualizar la tarea.")
    else:
        form = TareaForm(instance=task)



    user_groups = request.user.groups.values_list('name', flat=True)

    # Verificar si el usuario pertenece a los grupos específicos
    is_admin = 'admin' in user_groups
    is_supervisor = 'supervisor' in user_groups
    is_vendedor = 'vendedor' in user_groups

    context = {
        'is_admin': is_admin,
        'is_supervisor': is_supervisor,
        'is_vendedor': is_vendedor,
        'form': form,
    }

    return render(request, "dashboard/GestionTareas/crud/modify_task.html",context)

def deleteTask(request, id):
    task = get_object_or_404(Tarea, idTarea=id)
    task.delete()
    return redirect('gestion_task')


def detailTask(request):
    return render(request, "dashboard/GestionTareas/crud/detail.html")