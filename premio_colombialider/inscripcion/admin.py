'''
Created on 4/03/2011

@author: roque
'''
from django.contrib import admin
from premio_colombialider.inscripcion.models import *

admin.site.register(Tipogobernante)
admin.site.register(Departamento)
admin.site.register(Municipio)
admin.site.register(Medioconvocatoria)
admin.site.register(Inscrito)