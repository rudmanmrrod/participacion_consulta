# -*- coding: utf-8 -*-
"""
Sistema de Participación en Consultas

Copyleft (@) 2017 CENDITEL nodo Mérida - https://planificacion.cenditel.gob.ve/trac/wiki/ModeladoTopicos_2017
"""
## @package participacion.urls
#
# Urls de la aplicación participacion
# @author Rodrigo Boet (rboet at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
# @version 1.0
from django.urls import path
from .views import *

urlpatterns = [
    path('', ParticipacionIndex.as_view(), name = "participacion_index"),
    path('crear/<int:pk>', ParticipacionCreate.as_view(), name = "participacion_create"),
    path('crear/', ParticipacionCreate.as_view(), name = "participacion_create_nid"),
    path('mi-participacion', MiParticipacion.as_view(), name = "mi_participacion"),
]

## Ajax
urlpatterns +=[
    path('participacion/ajax/validar-participacion', validar_participacion, name = "participacion_validar"),
]