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
from django.conf.urls import url
from django.contrib.auth.views import *
from .views import *

urlpatterns = [
    url(r'^login$', LoginView.as_view(), name = "login"),
    url(r'^logout$', LogoutView.as_view(), name = "logout"),
    url(r'^register$', RegisterView.as_view(), name = "register"),
    #url(r'^update/(?P<pk>\d+)$', PerfilUpdate.as_view(), name = "update"),
]