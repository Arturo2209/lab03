"""
URL configuration for lab03_tarea project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from gestion import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('propietarios/nuevo/', views.registrar_propietario, name='registrar_propietario'),
    path('vehiculos/nuevo/', views.registrar_vehiculo, name='registrar_vehiculo'),
    path('vehiculos/<int:vehiculo_id>/eliminar/', views.eliminar_vehiculo, name='eliminar_vehiculo'),
    path('vehiculos/<int:vehiculo_id>/actualizar/', views.actualizar_vehiculo, name='actualizar_vehiculo'),
    path('registro/', views.mostrar_registros, name='mostrar_registros'),
    path('registros/nuevo/', views.registrar_registro, name='registrar_registro'),
    path('propietarios/<int:propietario_id>/', views.propietario_detalle, name='propietario_detalle'),
    path('propietarios/<int:propietario_id>/eliminar/', views.eliminar_propietario, name='eliminar_propietario'),
    path('vehiculos/<int:propietario_id>/', views.obtener_vehiculos, name='obtener_vehiculos'),
]
