from django.shortcuts import render,redirect
from .models import productos,tarea,usuario,UserProfile
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

        user = authenticate(request,username = usuario,password = clave)

        if user is not None:
            print("inicio correctamente")
            login(request,user)

            if user.groups.filter(name='administrador').exists():
                print("administrador")
                return redirect('admin_dashboard')
            elif user.groups.filter(name='supervisor').exists():
                print("supervisor")
                return redirect('supervisor_dashboard')
            elif user.groups.filter(name='vendedor').exists():
                print("vendedor")
                return redirect('vendedor_dashboard')
            else:
                context={
                    'error':'No tienes permisos para ingresar'
                }
                return render(request,'acceso/login.html',context)
        else:
            context={
                'error':'Error intente otra vez'
            }

            print("no inicio")

            print(request,user)
            return render(request,'acceso/login.html',context)
    return render(request,"acceso/login.html")




def registerView(request):
    data = {
        'form':CustomUserCreationForm()
    }
    if request.method == 'POST':
        user_creation_form =CustomUserCreationForm(data= request.POST)
        if user_creation_form.is_valid():
            user_creation_form.save()
            return redirect('login')

    return render(request,"dashboard/GestionUs/register.html",data)


def gestionarInformes(request):
    return render(request, "dashboard/GestionInfor/gestion_informes.html")


def logoutView(request):
    logout(request)
    return redirect('login')

def dashboardView(request):

    tareas = tarea.objects.all()
    context = {
        'tareas':tareas
    }
    
    return render(request, "dashboard/admin_dashboard.html",context)

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