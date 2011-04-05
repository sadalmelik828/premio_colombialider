from django.conf.urls.defaults import *
from premio_colombialider.inscripcion.views import *
from premio_colombialider.postulacion.views import *
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^premio_colombialider/', include('premio_colombialider.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    # *******************
    # urlCONF para archivos estaticos como css, js, imagenes y archivos
    (r'^multimedia/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': settings.MEDIA_ROOT}),
    # *******************
    (r'^$', index),
    (r'^acceso/$', ingreso),
    (r'^salir/$', salir),
    (r'^inscripcion/$', form_inscripcion),
    (r'^municipios/$', municipios),
    (r'^cambio_pass/$', cambio_pass),
    (r'^postulacion/(\d{1,4})/$', postulacion),
    (r'^evaluador/(\d{1,2})/$', evaluador),
    (r'^consultor/$', consultor),
    (r'^inscritos/$', inscritos),
    (r'^evaluaciones/$', evaluaciones),
)