from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    ##auth
    path('', views.loginView, name='login'),
    path('dashboard-admin/register/', views.register_view,name='register'),
    path('logout',views.logoutView,name='logout'),
    path('base',views.baseView,name='base'),
    ##Dashboards
    path('dashboard',views.dashboardView, name='admin_dashboard'),
    path('dashboard',views.supervisorView, name='supervisor_dashboard'),
    path('dashboard',views.vendedorView, name='vendedor_dashboard'),
    path('index',views.indexView, name='index'),
    path('dashboard-admin/Gestion_usuario',views.GestionUsuarioView, name='gestion_usuario'),
    ##Gestion de usuarios
    path('modifyUser',views.modifyUser,name='modifyuser'),
    path('createUser',views.createUser,name='createUser'),
    path('detailUser',views.detailView, name='detailUser'),
    ##Gestion de productos
    path('gestion-productos',views.gestionProd,name='gestion_productos'),
    path('detailProd',views.detailProd,name='detailProd'),
    path('modifyProd',views.modifyProd,name='modifyProd'),
    path('createProd',views.createProd,name='createProd'),
    ##Gestion de tareas
    path('gestion-tareas',views.gestionTask,name='gestion_task'),
    path('createTask',views.createTask,name='createTask'),
    path('modifyTask',views.modifyTask,name='modifyTask'),
    path('detailTask',views.detailTask,name='detailTask'),
    ##Gestion de informes
    path('gestion-informes',views.gestionarInformes,name='gestion_informes'),
    path('gestion-reportes/',views.solicitud_view, name= 'gestion_reportes'),
    path('lista-reportes/',views.lista_solicitudes, name= 'lista_solicitudes'),
    path('generarpdf/',views.generar_pdf, name='generar_pdf'),

]