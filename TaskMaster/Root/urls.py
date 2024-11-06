from django.urls import path
from . import views

urlpatterns = [
    ##auth
    path('', views.loginView, name='login'),
    path('register/', views.registerView,name='register'),
    path('logout',views.logoutView,name='logout'),
    ##Dashboards
    path('dashboard-admin',views.dashboardView, name='admin_dashboard'),
    path('dashboard-super',views.supervisorView, name='supervisor_dashboard'),
    path('dashboard-vend',views.vendedorView, name='vendedor_dashboard'),
    path('index',views.indexView, name='index'),
    ##Gestion de usuarios
    path('gestion-usuario',views.gestionUs,name='gestion_usuario'),
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

]