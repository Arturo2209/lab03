from django.shortcuts import render, redirect
from .models import Propietario, Vehiculo, Registro
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db import IntegrityError

def index(request):
    propietarios = Propietario.objects.all()
    return render(request, 'gestion/index.html', {'propietarios': propietarios})

def registrar_propietario(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        numero_apartamento = request.POST['numero_apartamento']
        telefono = request.POST['telefono']
        email = request.POST['email']

        # Validaciones
        if not nombre or not numero_apartamento or not telefono or not email:
            return render(request, 'gestion/propietario_form.html', {'error': 'Todos los campos son obligatorios.'})
        if not telefono.isdigit():
            return render(request, 'gestion/propietario_form.html', {'error': 'El teléfono debe contener solo números.'})

        # Verificar si el teléfono o el email ya están en uso
        if Propietario.objects.filter(telefono=telefono).exists():
            return render(request, 'gestion/propietario_form.html', {'error': 'Ya existe un propietario con ese número de teléfono.'})
        if Propietario.objects.filter(email=email).exists():
            return render(request, 'gestion/propietario_form.html', {'error': 'Ya existe un propietario con ese correo electrónico.'})

        try:
            Propietario.objects.create(
                nombre=nombre,
                numero_apartamento=numero_apartamento,
                telefono=telefono,
                email=email
            )
            return redirect('index')
        except IntegrityError:
            return render(request, 'gestion/propietario_form.html', {'error': 'Error al crear el propietario. Es posible que el teléfono o el correo ya estén en uso.'})

    return render(request, 'gestion/propietario_form.html')

def registrar_vehiculo(request):
    if request.method == 'POST':
        propietario_id = request.POST['propietario']
        matricula = request.POST['matricula']
        marca = request.POST['marca']
        modelo = request.POST['modelo']
        color = request.POST['color']
        
        # Validaciones
        if not matricula or not marca or not modelo or not color:
            return render(request, 'gestion/vehiculo_form.html', {'error': 'Todos los campos son obligatorios.'})

        # Verificar si la matrícula ya está en uso
        if Vehiculo.objects.filter(matricula=matricula).exists():
            return render(request, 'gestion/vehiculo_form.html', {'error': 'Ya existe un vehículo con esa matrícula.'})
        
        propietario = Propietario.objects.get(pk=propietario_id)

        try:
            Vehiculo.objects.create(
                propietario=propietario,
                matricula=matricula,
                marca=marca,
                modelo=modelo,
                color=color
            )
            return redirect('index')
        except IntegrityError:
            return render(request, 'gestion/vehiculo_form.html', {'error': 'Error al crear el vehículo. La matrícula ya podría estar en uso.'})

    propietarios = Propietario.objects.all()
    return render(request, 'gestion/vehiculo_form.html', {'propietarios': propietarios})

def registrar_registro(request):
    if request.method == 'POST':
        propietario_id = request.POST.get('propietario')
        vehiculo_id = request.POST.get('vehiculo')
        fecha_hora_entrada = request.POST.get('fecha_hora_entrada')
        fecha_hora_salida = request.POST.get('fecha_hora_salida')

        if not propietario_id or not vehiculo_id:
            return render(request, 'gestion/registro_form.html', {
                'error': 'El propietario y el vehículo son obligatorios.',
                'propietarios': Propietario.objects.all()
            })

        vehiculo = get_object_or_404(Vehiculo, pk=vehiculo_id)
        Registro.objects.create(
            vehiculo=vehiculo,
            fecha_hora_entrada=fecha_hora_entrada,
            fecha_hora_salida=fecha_hora_salida
        )
        return redirect('index')

    propietarios = Propietario.objects.all()
    return render(request, 'gestion/registro_form.html', {'propietarios': propietarios})


def propietario_detalle(request, propietario_id):
    propietario = Propietario.objects.get(pk=propietario_id)
    vehiculos = Vehiculo.objects.filter(propietario=propietario)
    return render(request, 'gestion/propietario_detalle.html', {'propietario': propietario, 'vehiculos': vehiculos})

def eliminar_propietario(request, propietario_id):
    propietario = Propietario.objects.get(pk=propietario_id)
    propietario.delete()
    return redirect('index')

def eliminar_vehiculo(request, vehiculo_id):
    vehiculo = get_object_or_404(Vehiculo, pk=vehiculo_id)
    vehiculo.delete()
    return redirect('propietario_detalle', propietario_id=vehiculo.propietario.id)

def actualizar_vehiculo(request, vehiculo_id):
    vehiculo = get_object_or_404(Vehiculo, pk=vehiculo_id)

    if request.method == 'POST':
        matricula = request.POST['matricula']
        marca = request.POST['marca']
        modelo = request.POST['modelo']
        color = request.POST['color']

        if not matricula or not marca or not modelo or not color:
            return render(request, 'gestion/vehiculo_form.html', {
                'vehiculo': vehiculo,
                'error': 'Todos los campos son obligatorios.'
            })

        # Actualizar solo los campos del vehículo
        vehiculo.matricula = matricula
        vehiculo.marca = marca
        vehiculo.modelo = modelo
        vehiculo.color = color
        vehiculo.save()
        return redirect('propietario_detalle', propietario_id=vehiculo.propietario.id)

    context = {
        'vehiculo': vehiculo,
    }
    return render(request, 'gestion/vehiculo_form.html', context)
def obtener_vehiculos(request, propietario_id):
    propietario = get_object_or_404(Propietario, pk=propietario_id)
    vehiculos = Vehiculo.objects.filter(propietario=propietario)
    vehiculos_data = [{'id': vehiculo.id, 'marca': vehiculo.marca, 'modelo': vehiculo.modelo, 'matricula': vehiculo.matricula} for vehiculo in vehiculos]
    return JsonResponse({'vehiculos': vehiculos_data})

def mostrar_registros(request):
    registros = Registro.objects.all().select_related('vehiculo__propietario')
    return render(request, 'gestion/mostrar_registros.html', {'registros': registros})

def registrar_vehiculo(request):
    if request.method == 'POST':
        propietario_id = request.POST['propietario']
        matricula = request.POST['matricula']
        marca = request.POST['marca']
        modelo = request.POST['modelo']
        color = request.POST['color']
        propietario = Propietario.objects.get(pk=propietario_id)
        Vehiculo.objects.create(
            propietario=propietario,
            matricula=matricula,
            marca=marca,
            modelo=modelo,
            color=color
        )
        return redirect('index')
    propietarios = Propietario.objects.all()
    return render(request, 'gestion/vehiculo_registro.html', {'propietarios': propietarios})

