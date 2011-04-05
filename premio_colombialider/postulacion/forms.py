# -*- coding: utf-8 -*-
'''
Created on 16/03/2011

@author: roque
'''
#import os
from django import forms
from django.contrib.admin import widgets
from premio_colombialider.postulacion.models import *

class RequisitoForm(forms.ModelForm):
    respuesta = forms.CharField(widget=forms.Textarea(attrs={'cols': 110}), required=False)
    anexo = forms.FileField(widget=widgets.AdminFileWidget(), help_text="Anexe el respectivo soporte en formato PDF.")
    class Meta:
        model = Postulacioncriteriorequisito
        exclude = ('criterio_requisito',)

class PreguntaForm(forms.ModelForm):
    respuesta = forms.CharField(widget=forms.Textarea(attrs={'cols': 105}), required=False)
    anexo = forms.FileField(widget=widgets.AdminFileWidget(), required=False, help_text="Anexe de manera opcional el soporte en formato PDF.")
    class Meta:
        model = Postulacionpreguntasubcategoriacategoria
        exclude = ('pregunta_subcategoria_categoria',)
        
class CriterioevaluacionForm(forms.ModelForm):
    respuesta = forms.CharField(widget=forms.Textarea(attrs={'cols': 105}), required=False)
    class Meta:
        model = Postulacionsubcategoriacategoriacriterioevaluacion
        exclude = ('criterio_evaluacion',)

class PostulacionForm(forms.ModelForm):
    plan_de_desarrollo = forms.FileField(widget=widgets.AdminFileWidget(), required=False)
    fotografias = forms.FileField(widget=widgets.AdminFileWidget(), required=False)
    matriculas_discapacidad = forms.FileField(widget=widgets.AdminFileWidget(), required=False)
    class Meta:
        model = Postulacion
        exclude = ('inscrito', 'postulacion_criterio_requisito', 'postulacion_pregunta_subcategoria_categoria',)