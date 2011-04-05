# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.contenttypes.models import ContentType
from premio_colombialider.inscripcion.models import Inscrito
from django.contrib.auth.models import User

# Create your models here.

ESCALA_CAL = (
              (1, '1'),
              (2, '2'),
              (3, '3'),
              (4, '4'),
              (5, '5'),
              (6, '6'),
              (7, '7'),
              (8, '8'),
              (9, '9'),
              (10, '10'),
              )
## Funcion que retorna la ruta dinamica de los anexos
def ruta_anexos(instancia, archivo):
    ctype = ContentType.objects.get_for_model(instancia)
    modelo = ctype.model
    if modelo == "postulacion":
        i = Inscrito.objects.get(pk=instancia.inscrito.id)
    else:
        i = Inscrito.objects.get(postulacion__pk=instancia.postulacion.id)
    u = i.usuario.username
    ext = archivo.split('.')
    nombre_archivo = str(u)+"_"+str(instancia.id)+"_"+modelo+"."+ext[-1].lower()
    return 'archivos/%s/%s' % (str(u), nombre_archivo)

class Categoria(models.Model):
    nombre = models.CharField(max_length=200)
    puntaje = models.PositiveIntegerField()
    
    class Meta:
        db_table = 'categoria'
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        
    def __unicode__(self):
        return '%s' % (self.nombre)

class Subcategoria(models.Model):
    nombre = models.TextField()
    subcategoria_categoria = models.ManyToManyField(Categoria, through='Subcategoriacategoria')
    
    class Meta:
        db_table = 'subcategoria'
        verbose_name = 'Subcategoría'
        verbose_name_plural = 'Subcategorías'
        
    def __unicode__(self):
        return '%s' % (self.nombre)

class Subcategoriacategoria(models.Model):
    subcategoria = models.ForeignKey(Subcategoria)
    categoria = models.ForeignKey(Categoria)
    puntaje = models.PositiveIntegerField(blank=True)
    
    class Meta:
        db_table = 'subcategoria_categoria'
        verbose_name = 'Categoría con subcategoría'
        verbose_name_plural = 'Categorías con subcategorías'
        unique_together = (('subcategoria', 'categoria'),)
    
    def __unicode__(self):
        return '%s -- %s' % (self.categoria.nombre, self.subcategoria.nombre)

class Pregunta(models.Model):
    nombre = models.TextField()
    pregunta_subcategoria_categoria = models.ManyToManyField(Subcategoriacategoria, through='Preguntasubcategoriacategoria')
    
    class Meta:
        db_table = 'pregunta'
        verbose_name = 'Pregunta'
        verbose_name_plural = 'Preguntas'
    
    def __unicode__(self):
        return '%s' % (self.nombre)

class Preguntasubcategoriacategoria(models.Model):
    pregunta = models.ForeignKey(Pregunta)
    subcategoria_categoria = models.ForeignKey(Subcategoriacategoria)
    puntaje = models.DecimalField(max_digits=12, decimal_places=9, blank=True)
    calificacion_maxima = models.IntegerField(choices=ESCALA_CAL)
    
    class Meta:
        db_table = 'pregunta_subcategoria_categoria'
        verbose_name = 'Pregunta de la subcategoría'
        verbose_name_plural = 'Preguntas de la subcategoría'
        unique_together = (('pregunta', 'subcategoria_categoria'),)
    
    def __unicode__(self):
        return '%s --- %s' % (self.subcategoria_categoria.subcategoria.nombre, self.pregunta.nombre)

class Criterioevaluacion(models.Model):
    nombre = models.CharField(max_length=200)
    
    class Meta:
        db_table = 'criterio_evaluacion'
        verbose_name = 'Criterio de evaluación'
        verbose_name_plural = 'Criterios de evaluación'
    
    def __unicode__(self):
        return '%s' % (self.nombre)

class Criteriorequisito(models.Model):
    nombre = models.TextField()
    
    class Meta:
        db_table = 'criterio_requisito'
        verbose_name = 'Criterio de requisitos'
        verbose_name_plural = 'Criterios de requisitos'
    
    def __unicode__(self):
        return '%s' % (self.nombre)

class Postulacion(models.Model):
    inscrito = models.ForeignKey(Inscrito, unique=True)
    plan_de_desarrollo = models.FileField(upload_to=ruta_anexos, blank=True)
    fotografias = models.FileField(upload_to=ruta_anexos, blank=True)
    matriculas_discapacidad = models.FileField(upload_to=ruta_anexos, blank=True)
    link_video_1 = models.URLField(verify_exists=False, blank=True)
    link_video_2 = models.URLField(verify_exists=False, blank=True)
    link_video_3 = models.URLField(verify_exists=False, blank=True)
    cerrada = models.BooleanField(default=False, verbose_name="Cerrar la postulación")
    postulacion_criterio_requisito = models.ManyToManyField(Criteriorequisito, through='Postulacioncriteriorequisito')    
    postulacion_pregunta_subcategoria_categoria = models.ManyToManyField(Preguntasubcategoriacategoria, through='Postulacionpreguntasubcategoriacategoria')
    
    class Meta:
        db_table = 'postulacion'
        verbose_name = 'Postulación'
        verbose_name_plural = 'Postulaciones'
    
    def __unicode__(self):
        return '%s' % (self.inscrito.nombre)

class Postulacioncriteriorequisito(models.Model):
    postulacion = models.ForeignKey(Postulacion)
    criterio_requisito = models.ForeignKey(Criteriorequisito)
    respuesta = models.TextField(blank=True)
    anexo = models.FileField(upload_to=ruta_anexos, blank=True)
    
    class Meta:
        db_table = 'postulacion_criterio_requisito'
        verbose_name = 'Requisito mínimo (Postulación)'
        verbose_name_plural = 'Requisitos mínimos (Postulación)'
        unique_together = (('postulacion', 'criterio_requisito'),)
    
    def __unicode__(self):
        return '%s' % (self.postulacion.inscrito.nombre)

class Postulacionsubcategoriacategoria(models.Model):
    postulacion = models.ForeignKey(Postulacion)
    subcategoria_categoria = models.ForeignKey(Subcategoriacategoria)
    postulacion_subcategoria_categoria_criterio_evaluacion = models.ManyToManyField(Criterioevaluacion, through="Postulacionsubcategoriacategoriacriterioevaluacion")
    
    class Meta:
        db_table = 'postulacion_subcategoria_categoria'
        verbose_name = 'Subcategoria postulación'
        verbose_name_plural = 'Subcategorias postulación'
        unique_together = (('postulacion', 'subcategoria_categoria'),)
        
    def __unicode__(self):
        return '%s -- %s -- %s' % (self.postulacion.inscrito.nombre, self.subcategoria_categoria.subcategoria.nombre, self.subcategoria_categoria.categoria.nombre)

class Postulacionsubcategoriacategoriacriterioevaluacion(models.Model):
    postulacion_subcategoria_categoria = models.ForeignKey(Postulacionsubcategoriacategoria)
    criterio_evaluacion = models.ForeignKey(Criterioevaluacion)
    respuesta = models.TextField(blank=True)
    
    class Meta:
        db_table = 'postulacion_subcategoria_categoria_criterio_evaluacion'
        verbose_name = 'Crit. evaluación subcategoría (Post.)'
        verbose_name_plural = 'Crit. evaluación subcategorias (Post.)'
        unique_together = (('postulacion_subcategoria_categoria', 'criterio_evaluacion'),)
    
    def __unicode__(self):
        return '%s' % (self.criterio_evaluacion.nombre)

class Postulacionpreguntasubcategoriacategoria(models.Model):
    postulacion = models.ForeignKey(Postulacion)
    pregunta_subcategoria_categoria = models.ForeignKey(Preguntasubcategoriacategoria)
    respuesta = models.TextField(blank=True)
    anexo = models.FileField(upload_to=ruta_anexos, blank=True)
    
    class Meta:
        db_table = 'postulacion_pregunta_subcategoria_categoria'
        verbose_name = 'Pregunta de postulación'
        verbose_name_plural = 'Preguntas de postulación'
        unique_together = (('postulacion', 'pregunta_subcategoria_categoria'),)
    
    def __unicode__(self):
        return '%s --- %s' % (self.pregunta_subcategoria_categoria.subcategoria_categoria.subcategoria.nombre,  self.pregunta_subcategoria_categoria.pregunta.nombre)

class Calificacionpostulacion(models.Model):
    usuario = models.ForeignKey(User)
    postulacion = models.ForeignKey(Postulacion)
    calificacion_extra = models.PositiveIntegerField(choices=ESCALA_CAL, blank=True)
    calificacion_postulacion_pregunta_subcategoria_categoria = models.ManyToManyField(Postulacionpreguntasubcategoriacategoria, through='Calificacionpostulacionpreguntasubcategoriacategoria')
    
    class Meta:
        db_table = 'calificacion_postulacion'
        verbose_name = 'Calificación de postulación'
        verbose_name = 'Calificaciones de postulaciones'
    
    def __unicode__(self):
        return '%s' % (self.postulacion.inscrito.nombre)

class Calificacionpostulacionpreguntasubcategoriacategoria(models.Model):
    calificacion_postulacion = models.ForeignKey(Calificacionpostulacion)
    postulacion_pregunta_subcategoria_categoria = models.ForeignKey(Postulacionpreguntasubcategoriacategoria)
    calificacion = models.IntegerField(choices=ESCALA_CAL, blank=True)
    
    class Meta:
        db_table = 'calificacion_postulacion_pregunta_subcategoria_categoria'
        verbose_name = 'Cal. preguntas de la postulación'
        verbose_name_plural = 'Cal. de las preguntas postulaciones'
        unique_together = (('calificacion_postulacion', 'postulacion_pregunta_subcategoria_categoria'),)
    
    def __unicode__(self):
        return '%s -- %s' % (self.postulacion_pregunta_subcategoria_categoria.pregunta_subcategoria_categoria.pregunta.nombre, self.calificacion)