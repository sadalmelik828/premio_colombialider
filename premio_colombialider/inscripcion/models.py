# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Tipogobernante(models.Model):
    nombre = models.CharField(max_length=25)
    
    class Meta:
        db_table = 'tipo_gobernante'
        verbose_name = 'Tipo de Gobernante'
        verbose_name_plural = 'Tipos de Gobernante'
        
    def __unicode__(self):
        return self.nombre
    
class Departamento(models.Model):    
    nombre = models.CharField(max_length=80)
    codigo = models.IntegerField()    

    class Meta:
        db_table = "departamento"
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'

    def __unicode__(self):
        return u'%s' % (self.nombre)

class Municipio(models.Model):
    nombre = models.CharField(max_length=80)
    codigo = models.IntegerField()
    poblacion = models.IntegerField()
    departamento = models.ForeignKey(Departamento)

    class Meta:
        db_table = "municipio"
        verbose_name = 'Municipio'
        verbose_name_plural = 'Municipios'
        ordering = ['departamento', 'nombre']

    def __unicode__(self):
        return u'%s (%s)' % (self.nombre, self.departamento.nombre)
    
class Medioconvocatoria(models.Model):
    nombre = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'medio_convocatoria'
        verbose_name = 'Medio de convocatoria'
        verbose_name_plural = 'Medios de convocatoria'
        
    def __unicode__(self):
        return self.nombre
    
class Inscrito(models.Model):
    tipo_gobernante = models.ForeignKey(Tipogobernante, verbose_name='Tipo de gobernante')
    municipio = models.ForeignKey(Municipio, verbose_name='Ciudad o Municipio')
    nombre = models.CharField(max_length=60, verbose_name='Nombre del alcalde o gobernador')
    tel_fijo = models.CharField(max_length=60, verbose_name='Teléfono fijo del alcalde o gobernador')
    celular = models.CharField(max_length=80, verbose_name='Número celular del alcalde o gobernador')
    correo = models.EmailField(verbose_name='Correo electrónico', help_text='Solo se aceptan correos que terminen en .gov.co')
    nombre_contacto = models.CharField(max_length=60, verbose_name='Nombre del contacto')
    cargo_contacto = models.CharField(max_length=60, verbose_name='Cargo del contacto')
    tel_fijo_contacto = models.CharField(max_length=60, verbose_name='Teléfono fijo del contacto')
    celular_contacto = models.CharField(max_length=80, verbose_name='Número celular del contacto')
    correo_contacto = models.EmailField(verbose_name='Correo electrónico del contacto')
    carta_postulacion = models.FileField(upload_to='archivos', verbose_name='Carta de postulación firmada por el alcalde o gobernador')
    medio_convocatoria = models.ManyToManyField(Medioconvocatoria, verbose_name='Por qué medio se enteró de esta convocatoria?')
    cual_medio = models.CharField(max_length=25, blank=True, null=True, verbose_name = 'Cúal medio?') 
    usuario = models.ForeignKey(User)
    
    class Meta:
        db_table = 'inscrito'
        verbose_name = 'Inscrito'
        verbose_name_plural = 'Inscritos'
        unique_together = ('tipo_gobernante', 'municipio',)
        
    def __unicode__(self):
        return "%s (%s - %s)" % (self.tipo_gobernante.nombre, self.municipio.departamento.nombre, self.municipio.nombre)