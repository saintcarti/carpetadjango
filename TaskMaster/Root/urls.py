from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginView, name='login'),
    path('register/', views.registerView,name='register'),
    path('dashboard-admin',views.dashboardView, name='admin_dashboard'),
    path('dashboard-super',views.supervisorView, name='supervisor_dashboard'),
    path('dashboard-vend',views.vendedorView, name='vendedor_dashboard'),
    path('index',views.indexView, name='index'),
    path('task', views.taskView, name='task'),
    path('detail',views.detailView, name='detail'),
    path('logout',views.logoutView,name='logout')
]