# -*- coding: utf-8 -*-
'''
Created on 24/02/2011

@author: roque
'''
import os
from django import forms
from premio_colombialider.inscripcion.models import Departamento, Tipogobernante, Medioconvocatoria

class InscritoForm(forms.Form):
    tipo_gobernante = forms.ModelChoiceField(label='Seleccione el tipo de Administración:', queryset=Tipogobernante.objects.all())
    departamento = forms.ModelChoiceField(label='Departamento', queryset=Departamento.objects.all().exclude(nombre='No Aplica'))
    municipio = forms.CharField(widget=forms.Select(), label='Ciudad o Municipio', help_text='Este campo depende de la selección del departamento.')
    nombre = forms.CharField(max_length=60, label='Nombre del alcalde o gobernador')
    tel_fijo = forms.CharField(max_length=60, label='Teléfono fijo del alcalde o gobernador')
    celular = forms.CharField(max_length=80, label='Número celular del alcalde o gobernador')
    correo = forms.EmailField(label='Correo electrónico del alcalde o gobernador', help_text='Solo se aceptan correos que terminen en .gov.co')
    nombre_contacto = forms.CharField(label='Nombre del contacto', max_length=60)
    cargo_contacto = forms.CharField(label='Cargo del  contacto', max_length=60)
    tel_fijo_contacto = forms.CharField(label='Teléfono fijo del contacto', max_length=60)
    celular_contacto = forms.CharField(label='Número celular del contacto', max_length=80)
    correo_contacto = forms.EmailField(label='Correo electrónico del contacto')
    carta_postulacion = forms.FileField(label='Carta de postulación firmada por el alcalde o gobernador', help_text='Solo se aceptan archivos en formato PDF.')    
    medio_convocatoria = forms.ModelMultipleChoiceField(label='Por qué medios se enteró de esta convocatoria?', queryset=Medioconvocatoria.objects.all(), widget=forms.CheckboxSelectMultiple())
    cual_medio = forms.CharField(widget=forms.TextInput(attrs={ 'disabled': 'disabled' }), label='Cúal medio?', help_text="Diligencie este campo en caso de seleccionar 'Otro' en los medios por donde se enteró de la convocatoria.", required=False)
    
    def clean_carta_postulacion(self):
        f = self.cleaned_data['carta_postulacion']
        extension_valida = ('pdf')
        contenido_valido = ('application/pdf')
        ext = os.path.splitext(f.name)[1][1:].lower()
        if ext in extension_valida and f.content_type in contenido_valido:
            if f.size > 2621440:
                raise forms.ValidationError('El valor máximo de un archivo son 2.5 MB.')
            else:
                return f
        raise forms.ValidationError('El tipo de documento no es válido. Solo se acepta .pdf.')

class CambiopassForm(forms.Form):
    v_pass = forms.CharField(label='Contraseña actual', widget=forms.PasswordInput)
    n_pass = forms.CharField(label='Contraseña nueva', widget=forms.PasswordInput)
    cn_pass = forms.CharField(label='Confirmación contraseña nueva', widget=forms.PasswordInput)
    
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(CambiopassForm, self).__init__(*args, **kwargs)
        
    def clean_v_pass(self):
        vp = self.cleaned_data['v_pass']
        if not self.user.check_password(vp):
            raise forms.ValidationError('Su contraseña actual es incorrecta. Por favor intente de nuevo.')
        return vp
    
    def clean_cn_pass(self):
        np = self.cleaned_data['n_pass']
        cnp = self.cleaned_data['cn_pass']
        if np != cnp:
            raise forms.ValidationError('La confirmación de la contraseña nueva no coincide.')
        return cnp
    
    def save(self, commit=True):
        n_pass = self.cleaned_data['n_pass']
        self.user.set_password(n_pass)
        if commit:
            self.user.save()
        return self.user