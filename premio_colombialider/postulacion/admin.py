# -*- coding: utf-8 -*-
'''
Created on 4/03/2011

@author: roque
'''
from django.contrib import admin
from premio_colombialider.postulacion.models import *

class SubcategoriacategoriaAdmin(admin.ModelAdmin):
    list_display = ('categoria', 'subcategoria', 'puntaje',)

class PreguntasubcategoriacategoriaAdmin(admin.ModelAdmin):
    list_display = ('pregunta', 'subcategoria_categoria', 'puntaje', 'calificacion_maxima',)
    
class PostulacioncriteriorequisitoInline(admin.TabularInline):
    model = Postulacioncriteriorequisito
    max_num = 2
    verbose_name = 'Requisito mínimo'
    verbose_name_plural = 'Requisitos mínimos'

class PostulacionpreguntasubcategoriacategoriaInline(admin.TabularInline):
    model = Postulacionpreguntasubcategoriacategoria
    max_num = 35
    verbose_name = 'Pregunta de postulación'
    verbose_name_plural = 'Preguntas de postulación'

class PostulacionAdmin(admin.ModelAdmin):
    inlines = [PostulacioncriteriorequisitoInline, PostulacionpreguntasubcategoriacategoriaInline]
    
admin.site.register(Categoria)
admin.site.register(Subcategoria)
admin.site.register(Subcategoriacategoria, SubcategoriacategoriaAdmin)
admin.site.register(Pregunta)
admin.site.register(Preguntasubcategoriacategoria, PreguntasubcategoriacategoriaAdmin)
admin.site.register(Criterioevaluacion)
admin.site.register(Criteriorequisito)
admin.site.register(Postulacion, PostulacionAdmin)
admin.site.register(Postulacioncriteriorequisito)
admin.site.register(Postulacionpreguntasubcategoriacategoria)
admin.site.register(Calificacionpostulacion)
admin.site.register(Calificacionpostulacionpreguntasubcategoriacategoria)
