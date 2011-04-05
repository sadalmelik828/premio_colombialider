# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from premio_colombialider.inscripcion.models import *
from premio_colombialider.postulacion.models import *
from premio_colombialider.postulacion.forms import *
from django.forms.models import inlineformset_factory, modelformset_factory
from django.forms.formsets import formset_factory

def postulacion(request, inscrito):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/acceso/')
    else:
        vm = ''
        msg = ''
        if 'msg' in request.GET:
            vm = request.GET['msg']
        if vm == '1':
            msg = "Los datos se han guardado."
        if vm == '2':
            msg = "La contraseña se ha cambiado."
        ins = Inscrito.objects.select_related(depth=3).get(pk=inscrito)
        postulacion = Postulacion.objects.get(inscrito__pk=inscrito)        
        ### requisitos ###
        req = Criteriorequisito.objects.only('nombre')
        r = inlineformset_factory(Postulacion, Postulacioncriteriorequisito, form=RequisitoForm, can_delete=False, max_num=req.count())        
        ### categoria resultados ###
        # subcategoria educacion
        edu = Postulacionpreguntasubcategoriacategoria.objects.filter(pregunta_subcategoria_categoria__subcategoria_categoria__pk=1) 
        e = inlineformset_factory(Postulacion, Postulacionpreguntasubcategoriacategoria, form=PreguntaForm, can_delete=False, max_num=edu.count())
        qcee = Postulacionsubcategoriacategoriacriterioevaluacion.objects.filter(postulacion_subcategoria_categoria__postulacion=postulacion, postulacion_subcategoria_categoria__subcategoria_categoria__pk=1)
        qfcee = inlineformset_factory(Postulacionsubcategoriacategoria, Postulacionsubcategoriacategoriacriterioevaluacion, form=CriterioevaluacionForm, can_delete=False, max_num=qcee.count())
        # subcategoria Mercado laboral y productividad
        mer = Postulacionpreguntasubcategoriacategoria.objects.filter(pregunta_subcategoria_categoria__subcategoria_categoria__pk=2)
        m = inlineformset_factory(Postulacion, Postulacionpreguntasubcategoriacategoria, form=PreguntaForm, can_delete=False, max_num=mer.count())
        qcem = Postulacionsubcategoriacategoriacriterioevaluacion.objects.filter(postulacion_subcategoria_categoria__postulacion=postulacion, postulacion_subcategoria_categoria__subcategoria_categoria__pk=2)
        qfcem = inlineformset_factory(Postulacionsubcategoriacategoria, Postulacionsubcategoriacategoriacriterioevaluacion, form=CriterioevaluacionForm, can_delete=False, max_num=qcem.count())
        # Accesibilidad
        acc = Postulacionpreguntasubcategoriacategoria.objects.filter(pregunta_subcategoria_categoria__subcategoria_categoria__pk=3)
        a = inlineformset_factory(Postulacion, Postulacionpreguntasubcategoriacategoria, form=PreguntaForm, can_delete=False, max_num=acc.count())
        qcea = Postulacionsubcategoriacategoriacriterioevaluacion.objects.filter(postulacion_subcategoria_categoria__postulacion=postulacion, postulacion_subcategoria_categoria__subcategoria_categoria__pk=3)
        qfcea = inlineformset_factory(Postulacionsubcategoriacategoria, Postulacionsubcategoriacategoriacriterioevaluacion, form=CriterioevaluacionForm, can_delete=False, max_num=qcea.count())
        # Acceso a la informacion
        ac = Postulacionpreguntasubcategoriacategoria.objects.filter(pregunta_subcategoria_categoria__subcategoria_categoria__pk=4)
        ai = inlineformset_factory(Postulacion, Postulacionpreguntasubcategoriacategoria, form=PreguntaForm, can_delete=False, max_num=ac.count())
        qcei = Postulacionsubcategoriacategoriacriterioevaluacion.objects.filter(postulacion_subcategoria_categoria__postulacion=postulacion, postulacion_subcategoria_categoria__subcategoria_categoria__pk=4)
        qfcei = inlineformset_factory(Postulacionsubcategoriacategoria, Postulacionsubcategoriacategoriacriterioevaluacion, form=CriterioevaluacionForm, can_delete=False, max_num=qcei.count())
        # Convivencia y derechos humanos
        hum = Postulacionpreguntasubcategoriacategoria.objects.filter(pregunta_subcategoria_categoria__subcategoria_categoria__pk=5)
        c = inlineformset_factory(Postulacion, Postulacionpreguntasubcategoriacategoria, form=PreguntaForm, can_delete=False, max_num=hum.count())
        qcec = Postulacionsubcategoriacategoriacriterioevaluacion.objects.filter(postulacion_subcategoria_categoria__postulacion=postulacion, postulacion_subcategoria_categoria__subcategoria_categoria__pk=5)
        qfcec = inlineformset_factory(Postulacionsubcategoriacategoria, Postulacionsubcategoriacategoriacriterioevaluacion, form=CriterioevaluacionForm, can_delete=False, max_num=qcec.count())
        # Cultura, recreacion y deporte
        cul = Postulacionpreguntasubcategoriacategoria.objects.filter(pregunta_subcategoria_categoria__subcategoria_categoria__pk=6)
        crd = inlineformset_factory(Postulacion, Postulacionpreguntasubcategoriacategoria, form=PreguntaForm, can_delete=False, max_num=cul.count())
        qced = Postulacionsubcategoriacategoriacriterioevaluacion.objects.filter(postulacion_subcategoria_categoria__postulacion=postulacion, postulacion_subcategoria_categoria__subcategoria_categoria__pk=6)
        qfced = inlineformset_factory(Postulacionsubcategoriacategoria, Postulacionsubcategoriacategoriacriterioevaluacion, form=CriterioevaluacionForm, can_delete=False, max_num=qced.count())
        # Registro de localizacion y caracterizacion de personas con discapacidad
        loc = Postulacionpreguntasubcategoriacategoria.objects.filter(pregunta_subcategoria_categoria__subcategoria_categoria__pk=7)
        l = inlineformset_factory(Postulacion, Postulacionpreguntasubcategoriacategoria, form=PreguntaForm, can_delete=False, max_num=loc.count())
        qcel = Postulacionsubcategoriacategoriacriterioevaluacion.objects.filter(postulacion_subcategoria_categoria__postulacion=postulacion, postulacion_subcategoria_categoria__subcategoria_categoria__pk=7)
        qfcel = inlineformset_factory(Postulacionsubcategoriacategoria, Postulacionsubcategoriacategoriacriterioevaluacion, form=CriterioevaluacionForm, can_delete=False, max_num=qcel.count())
        # Otros sectores
        sec = Postulacionpreguntasubcategoriacategoria.objects.filter(pregunta_subcategoria_categoria__subcategoria_categoria__pk=8)
        o = inlineformset_factory(Postulacion, Postulacionpreguntasubcategoriacategoria, form=PreguntaForm, can_delete=False, max_num=sec.count())
        qces = Postulacionsubcategoriacategoriacriterioevaluacion.objects.filter(postulacion_subcategoria_categoria__postulacion=postulacion, postulacion_subcategoria_categoria__subcategoria_categoria__pk=8)
        qfces = inlineformset_factory(Postulacionsubcategoriacategoria, Postulacionsubcategoriacategoriacriterioevaluacion, form=CriterioevaluacionForm, can_delete=False, max_num=qces.count())
        ### Categoria gestion integral ###
        ges = Postulacionpreguntasubcategoriacategoria.objects.filter(pregunta_subcategoria_categoria__subcategoria_categoria__pk=9)
        g = inlineformset_factory(Postulacion, Postulacionpreguntasubcategoriacategoria, form=PreguntaForm, can_delete=False, max_num=ges.count())
        ### Categoria replicabilidad ###
        rep = Postulacionpreguntasubcategoriacategoria.objects.filter(pregunta_subcategoria_categoria__subcategoria_categoria__pk=10)
        d = inlineformset_factory(Postulacion, Postulacionpreguntasubcategoriacategoria, form=PreguntaForm, can_delete=False, max_num=rep.count())
        ### Categoria Innovacion ###
        inn = Postulacionpreguntasubcategoriacategoria.objects.filter(pregunta_subcategoria_categoria__subcategoria_categoria__pk=11)
        i = inlineformset_factory(Postulacion, Postulacionpreguntasubcategoriacategoria, form=PreguntaForm, can_delete=False, max_num=inn.count())
        ### Categoria Participacion ###
        part = Postulacionpreguntasubcategoriacategoria.objects.filter(pregunta_subcategoria_categoria__subcategoria_categoria__pk=12)
        t = inlineformset_factory(Postulacion, Postulacionpreguntasubcategoriacategoria, form=PreguntaForm, can_delete=False, max_num=part.count())
        if request.method == "POST":
            p = PostulacionForm(request.POST, request.FILES, instance=postulacion)            
            requisitos = r(request.POST, request.FILES, instance=postulacion)
            educacion = e(request.POST, request.FILES, instance=postulacion, queryset=edu, prefix="educacion")
            fcee = qfcee(request.POST, instance=qcee[0].postulacion_subcategoria_categoria, queryset=qcee, prefix="fcee")
            mercado = m(request.POST, request.FILES, instance=postulacion, queryset=mer, prefix="mercado")
            fcem = qfcem(request.POST, instance=qcem[0].postulacion_subcategoria_categoria, queryset=qcem, prefix="fcem")
            accesibilidad = a(request.POST, request.FILES, instance=postulacion, queryset=acc, prefix="accesibilidad")
            fcea = qfcea(request.POST, instance=qcea[0].postulacion_subcategoria_categoria, queryset=qcea, prefix="fcea")
            acceso = ai(request.POST, request.FILES, instance=postulacion, queryset=ac, prefix="acceso")
            fcei = qfcei(request.POST, instance=qcei[0].postulacion_subcategoria_categoria, queryset=qcei, prefix="fcei")
            convivencia = c(request.POST, request.FILES, instance=postulacion, queryset=hum, prefix="convivencia")
            fcec = qfcec(request.POST, instance=qcec[0].postulacion_subcategoria_categoria, queryset=qcec, prefix="fcec")
            cultura = crd(request.POST, request.FILES, instance=postulacion, queryset=cul, prefix="cultura")
            fced = qfced(request.POST, instance=qced[0].postulacion_subcategoria_categoria, queryset=qced, prefix="fced")
            registro = l(request.POST, request.FILES, instance=postulacion, queryset=loc, prefix="registro")
            fcel = qfcel(request.POST, instance=qcel[0].postulacion_subcategoria_categoria, queryset=qcel, prefix="fcel")
            sectores = o(request.POST, request.FILES, instance=postulacion, queryset=sec, prefix="sectores")
            fces = qfces(request.POST, instance=qces[0].postulacion_subcategoria_categoria, queryset=qces, prefix="fces")
            gestion = g(request.POST, request.FILES, instance=postulacion, queryset=ges, prefix="gestion")
            replicabilidad = d(request.POST, request.FILES, instance=postulacion, queryset=rep, prefix="replicabilidad")
            innovacion = i(request.POST, request.FILES, instance=postulacion, queryset=inn, prefix="innovacion")
            participacion = t(request.POST, request.FILES, instance=postulacion, queryset=part, prefix="participacion")
            if p.is_valid() and requisitos.is_valid() and educacion.is_valid() and fcee.is_valid() and mercado.is_valid() and fcem.is_valid() and accesibilidad.is_valid() and fcea.is_valid() and acceso.is_valid() and fcei.is_valid() and convivencia.is_valid() and fcec.is_valid() and cultura.is_valid() and fced.is_valid() and registro.is_valid() and fcel.is_valid() and sectores.is_valid() and fces.is_valid() and gestion.is_valid() and replicabilidad.is_valid() and innovacion.is_valid() and participacion.is_valid():
                p.save()
                requisitos.save()
                educacion.save()
                fcee.save()
                mercado.save()
                fcem.save()
                accesibilidad.save()
                fcea.save()
                acceso.save()
                fcei.save()
                convivencia.save()
                fcec.save()
                cultura.save()
                fced.save()
                registro.save()
                fcel.save()
                sectores.save()
                fces.save()
                gestion.save()
                replicabilidad.save()
                innovacion.save()
                participacion.save()
                return HttpResponseRedirect("/postulacion/"+str(inscrito)+"?msg=1")
        else:
            p = PostulacionForm(instance=postulacion)
            requisitos = r(instance=postulacion)
            educacion = e(instance=postulacion, queryset=edu, prefix="educacion")
            fcee = qfcee(instance=qcee[0].postulacion_subcategoria_categoria, queryset=qcee, prefix="fcee")
            mercado = m(instance=postulacion, queryset=mer, prefix="mercado")
            fcem = qfcem(instance=qcem[0].postulacion_subcategoria_categoria, queryset=qcem, prefix="fcem")
            accesibilidad = a(instance=postulacion, queryset=acc, prefix="accesibilidad")
            fcea = qfcea(instance=qcea[0].postulacion_subcategoria_categoria, queryset=qcea, prefix="fcea")
            acceso = ai(instance=postulacion, queryset=ac, prefix="acceso")
            fcei = qfcei(instance=qcei[0].postulacion_subcategoria_categoria, queryset=qcei, prefix="fcei")
            convivencia = c(instance=postulacion, queryset=hum, prefix="convivencia")
            fcec = qfcec(instance=qcec[0].postulacion_subcategoria_categoria, queryset=qcec, prefix="fcec")
            cultura = crd(instance=postulacion, queryset=cul, prefix="cultura")
            fced = qfced(instance=qced[0].postulacion_subcategoria_categoria, queryset=qced, prefix="fced")
            registro = l(instance=postulacion, queryset=loc, prefix="registro")
            fcel = qfcel(instance=qcel[0].postulacion_subcategoria_categoria, queryset=qcel, prefix="fcel")
            sectores = o(instance=postulacion, queryset=sec, prefix="sectores")
            fces = qfces(instance=qces[0].postulacion_subcategoria_categoria, queryset=qces, prefix="fces")
            gestion = g(instance=postulacion, queryset=ges, prefix="gestion")
            replicabilidad = d(instance=postulacion, queryset=rep, prefix="replicabilidad")
            innovacion = i(instance=postulacion, queryset=inn, prefix="innovacion")
            participacion = t(instance=postulacion, queryset=part, prefix="participacion")
        return render_to_response('postulacion/postulacion.html', {
                                                                   'inscrito': ins,
                                                                   'postulacion': p,
                                                                   'requisitos': requisitos, 
                                                                   'educacion': educacion, 
                                                                   'mercado': mercado, 
                                                                   'accesibilidad': accesibilidad, 
                                                                   'acceso': acceso, 
                                                                   'convivencia': convivencia, 
                                                                   'cultura': cultura, 
                                                                   'registro': registro, 
                                                                   'sectores': sectores, 
                                                                   'req': req, 
                                                                   'edu': edu, 
                                                                   'mer': mer, 
                                                                   'acc': acc, 
                                                                   'ac': ac, 
                                                                   'hum': hum, 
                                                                   'cul': cul, 
                                                                   'loc': loc, 
                                                                   'sec': sec, 
                                                                   'replicabilidad': replicabilidad, 
                                                                   'rep': rep,
                                                                   'innovacion': innovacion,
                                                                   'inn': inn,
                                                                   'participacion': participacion,
                                                                   'part': part,
                                                                   'gestion': gestion,
                                                                   'ges': ges,
                                                                   'fcee': fcee,
                                                                   'fcem': fcem,
                                                                   'fcea': fcea,
                                                                   'fcei': fcei,
                                                                   'fcec': fcec,
                                                                   'fced': fced,
                                                                   'fcel': fcel,
                                                                   'fces': fces,
                                                                   'msg': msg
                                                                    })

def evaluador(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/acceso/')
    else:
        return render_to_response('postulacion/evaluador.html')

def consultor(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/acceso/')
    else:
        return render_to_response('postulacion/consultor.html')
    
def inscritos(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/acceso/')
    else:
        p = Postulacion.objects.select_related().extra(select={"estado_diligenciamiento": "(select count(*) from postulacion_criterio_requisito r where r.postulacion_id = postulacion.id and (r.respuesta = '' or r.anexo = ''))+(select count(*) from postulacion_pregunta_subcategoria_categoria pr where pr.postulacion_id = postulacion.id and pr.respuesta = '')+(select count(*) from postulacion_pregunta_subcategoria_categoria a where a.postulacion_id = postulacion.id and a.pregunta_subcategoria_categoria_id in (2,8,13,18,25,26,32,37) group by a.anexo having a.anexo = '')"},)
        return render_to_response('postulacion/inscritos.html', { 'inscritos': p })
    
def evaluaciones(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/acceso/')
    else:
        return render_to_response('postulacion/evaluaciones.html')