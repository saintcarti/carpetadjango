from django.shortcuts import render,redirect
from .models import productos,tarea,usuario,UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm
from django.contrib.auth.models import Group





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

    return render(request,"acceso/register.html",data)

def logoutView(request):
    logout(request)
    return redirect('login')

@login_required
def dashboardView(request):
    tareas = tarea.objects.all()
    context = {
        'tareas':tareas
    }
    
    return render(request, "dashboard/admin_dashboard.html",context)

@login_required
def supervisorView(request):
    return render(request, "dashboard/supervisor_dashboard.html")

@login_required
def vendedorView(request):
    return render(request, "dashboard/vendedor_dashboard.html")


def taskView(request):
    return render(request, "dashboard/task.html")

def detailView(request):
    return render(request, "dashboard/detail.html")