# -*- coding: utf-8 -*-
import os, stat
from random import choice
from django.conf import settings
from premio_colombialider.inscripcion.models import Inscrito, Municipio, Departamento, Tipogobernante
from premio_colombialider.postulacion.models import *
from premio_colombialider.inscripcion.forms import InscritoForm, CambiopassForm
from django.contrib.auth.models import User, Group
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson
from django.core.mail import *

def manejador_archivos(archivo, usuario):
    carpeta = os.path.join(settings.MEDIA_ROOT+'/archivos/', usuario)
    if not os.path.isdir(carpeta):
        os.mkdir(carpeta)
        os.chmod(carpeta, stat.S_IRWXU)
    ext = os.path.splitext(archivo.name)
    nombre_archivo = "/"+usuario+"_carta_postulacion"+ext[1].lower()
    ruta = open(carpeta+nombre_archivo, 'wb+')
    for c in archivo.chunks():
        ruta.write(c)
    ruta.close()
    return 'archivos/%s%s' % (usuario, nombre_archivo)

def index(request):
    msg = ''
    vm = ''
    if 'msg' in request.GET:
        vm = request.GET['msg']
        if vm == '1':
            msg = "Felicidades, revise su correo."
    return render_to_response('inscripcion/index.html', { 'msg': msg })

def form_inscripcion(request):    
    if request.method == 'POST':
        formulario = InscritoForm(request.POST, request.FILES)
        if formulario.is_valid():
            ### creación del usuario en django.contrib.auth para dar acceso al aplicativo ###
            caracteres = 'abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789'
            username = ''.join([choice(caracteres) for i in range(6)])
            clave = ''.join([choice(caracteres) for i in range(10)])
            usuario = User.objects.create_user(username, request.POST['correo_contacto'], clave)
            grupo = Group.objects.get(pk=1)
            usuario.groups.add(grupo)
            mpo = Municipio.objects.get(pk=request.POST['municipio'])
            g = request.POST['tipo_gobernante']
            if g == '1':
                usuario.first_name = 'Gobernador(a) de '
                depto = Departamento.objects.get(pk=request.POST['departamento'])
                usuario.last_name = depto.nombre
            else:
                usuario.first_name = 'Alcalde(sa) de '
                usuario.last_name = str(mpo)
            usuario.save()
            ### Subida del archivo al servidor ###
            carta = request.FILES['carta_postulacion']
            ruta_archivo = manejador_archivos(carta, username)
            ### creación del registro en inscritos ###
            medio = ''
            if 'cual_medio' in request.POST:
                medio = request.POST['cual_medio']
            reg = Inscrito(nombre=request.POST['nombre'], tel_fijo=request.POST['tel_fijo'], celular=request.POST['celular'], correo=request.POST['correo'], nombre_contacto=request.POST['nombre_contacto'], cargo_contacto=request.POST['cargo_contacto'], tel_fijo_contacto=request.POST['tel_fijo_contacto'], celular_contacto=request.POST['celular_contacto'], correo_contacto=request.POST['correo_contacto'], carta_postulacion=ruta_archivo)
            gob = Tipogobernante.objects.get(pk=request.POST['tipo_gobernante'])
            reg.municipio = mpo
            reg.tipo_gobernante = gob
            reg.usuario = usuario
            reg.cual_medio = medio
            reg.save()
            for i in request.POST.getlist('medio_convocatoria'):
                reg.medio_convocatoria.add(i)
            ### creacion de registros de postulacion ###
            # creacion postulacion
            postulacion = Postulacion(inscrito=reg)
            postulacion.save()
            # creacion de requisitos a la postulacion
            requisitos = Criteriorequisito.objects.all()
            for req in requisitos:
                cr = Postulacioncriteriorequisito.objects.create(postulacion=postulacion, criterio_requisito=req)
                cr.save()
            # creacion de subcategorias de la categoria resultados a la postulacion
            sub_resultados = Subcategoriacategoria.objects.filter(categoria__pk=1)
            for csr in sub_resultados:
                sr = Postulacionsubcategoriacategoria.objects.create(postulacion=postulacion, subcategoria_categoria=csr)
                sr.save()
            post_sub_cat = Postulacionsubcategoriacategoria.objects.filter(postulacion=postulacion)
            criterios_evaluacion = Criterioevaluacion.objects.all()
            for cpsc in post_sub_cat:
                for cce in criterios_evaluacion:
                    ce = Postulacionsubcategoriacategoriacriterioevaluacion.objects.create(postulacion_subcategoria_categoria=cpsc, criterio_evaluacion=cce)
                    ce.save()
            # creacion de todas las preguntas a la postulacion
            preguntas = Preguntasubcategoriacategoria.objects.all()
            for psc in preguntas:
                s = Postulacionpreguntasubcategoriacategoria.objects.create(postulacion=postulacion, pregunta_subcategoria_categoria=psc)
                s.save()
            # Envio de mail para notificar inscripción y codigos de acceso al aplicativo
            asunto = 'Postulación Premio Colombia Líder'            
            mensaje = "<h3>COLOMBIA L&Iacute;DER - PREMIO A LOS MEJORES ALCALDES Y GOBERNADORES 2008 - 2011</h3><p>Cordial Saludo,</p>"
            mensaje += "<p align='justify'>Colombia L&iacute;der le da la bienvenida a la plataforma de postulaci&oacute;n al premio a los mejores alcaldes y gobernadores 2008 - 2011. Para acceder a la plataforma usted debe ingresar a la siguiente direcci&oacute;n web:<br><br><a target='_blank' href='http://premioag.colombialider.org/'>http://premioag.colombialider.org/</a><br><br>En ella le será solicitado un usuario y contrase&ntilde;a, para lo cual debe utilizar los datos que le suministra la plataforma a continuaci&oacute;n:<br><br>Usuario: <b>"+username+"</b><br>Contrase&ntilde;a: <b>"+clave+"</b></p>"
            mensaje += "<p align='justify'>Recuerde que este usuario ser&aacute; el que debe utilizar en el proceso de postulaci&oacute;n, es personal e intransferible, por lo tanto le recomendamos que cuando ingrese por primera vez cambie su contrase&ntilde;a para mayor seguridad. Esto lo podr&aacute; realizar en el panel de postulaci&oacute;n en un link que indica cambiar la contrase&ntilde;a.</p>"
            mensaje += "Mayores informes: Karem Labrador, Coordinadora General de Colombia Líder - Celular: 301 700 7459 - correo electr&oacute;nico: premio@colombialider.org - inclusion@colombialider.org"
            msg = EmailMessage(asunto, mensaje, settings.DEFAULT_FROM_EMAIL, [request.POST['correo'], request.POST['correo_contacto']])
            msg.content_subtype = 'html'
            msg.send()
            return HttpResponseRedirect('/?msg=1')
    else:
        formulario = InscritoForm()
    return render_to_response('inscripcion/formulario.html', { 'formulario': formulario })

def municipios(request):
    datos = [{ 'id': '', 'nombre': '---------' }]
    cant = Departamento.objects.filter(pk=request.POST['depto_id']).count()
    if cant > 0:
        mpos = Municipio.objects.filter(departamento__pk=request.POST['depto_id'])
        for k in mpos:
            datos.append({ 'id': k.id, 'nombre': k.nombre, 'codigo': k.codigo })
    respuesta = simplejson.dumps(datos)
    return HttpResponse(respuesta, mimetype='application/json')

def ingreso(request):
    if request.method == 'POST':
        nick = request.POST['usuario']
        password = request.POST['password']
        user = authenticate(username=nick, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                usuario = User.objects.get(username__exact=nick)
                g = usuario.groups.all()
                if g[0].id == 1:
                    inscrito = usuario.inscrito_set.all()
                    return HttpResponseRedirect("/postulacion/"+str(inscrito[0].id))
                elif g[0].id == 2:
                    return HttpResponseRedirect("/evaluador/"+str(usuario.id))
                else:
                    return HttpResponseRedirect('/consultor/')
            else:
                msg = 'El usuario con el que intenta ingresar no esta activo.'
            return render_to_response('inscripcion/acceso.html', {'msg': msg})
        else:
            msg = 'El usuario o contraseña son incorrectos.'
            return render_to_response('inscripcion/acceso.html', {'msg': msg})
    else:
        return render_to_response('inscripcion/acceso.html')

def salir(request):
    logout(request)
    return HttpResponseRedirect('/')

def cambio_pass(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/acceso/')
    else:    
        if request.method == 'POST':
            formulario = CambiopassForm(user=request.user, data=request.POST)
            if formulario.is_valid():
                formulario.save()
                usuario = User.objects.get(username__exact=request.user)
                g = usuario.groups.all()
                if g[0].id == 1:
                    inscrito = usuario.inscrito_set.all()
                    return HttpResponseRedirect("/postulacion/"+str(inscrito[0].id)+"?msg=2")
                elif g[0].id == 2:
                    return HttpResponseRedirect("/evaluador/"+str(usuario.id))
                else:
                    return HttpResponseRedirect('/consultor/')
        else:
            formulario = CambiopassForm(user=request.user)
        return render_to_response('inscripcion/cambio_pass.html', { 'formulario': formulario })