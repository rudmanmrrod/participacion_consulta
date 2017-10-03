# -*- coding: utf-8 -*-
"""
Sistema de Participación en Consultas

Copyleft (@) 2017 CENDITEL nodo Mérida - https://planificacion.cenditel.gob.ve/trac/wiki/ModeladoTopicos_2017
"""
## @package base.views
#
# Vistas correspondientes a la aplicación base
# @author Rodrigo Boet (rboet at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
# @version 1.0
from django.shortcuts import render
from django.http import JsonResponse
from django.apps import apps
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from base.functions import cargar_municipios, cargar_parroquias

import json
 
class Inicio(TemplateView):
    """!
    Clase para mostrar el inicio del sistema

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 24-04-2017
    @version 1.0.0
    """
    template_name = "inicio.html"


def buscar_municipio(request):
    """!
    Función buscar municipios (se puede filtrar por la entidad)

    @author Rodrigo Boet (robet at cenditel.gob.ve)
    @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 03-10-2017
    @param request <b>{object}</b> Objeto que contiene la petición
    @return Devuelve un JsonResponse con los datos
    """
    entidad = request.GET.get('entidad',None)
    if(entidad):
        data = cargar_municipios(entidad)
    else:
        data = cargar_municipios()
    return JsonResponse(data,safe=False)

def buscar_parroquia(request):
    """!
    Función buscar parroquias (se puede filtrar por el municipio)

    @author Rodrigo Boet (robet at cenditel.gob.ve)
    @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 03-10-2017
    @param request <b>{object}</b> Objeto que contiene la petición
    @return Devuelve un JsonResponse con los datos
    """
    municipio = request.GET.get('municipio',None)
    if(municipio):
        data = cargar_parroquias(municipio)
    else:
        data = cargar_parroquias()
    return JsonResponse(data,safe=False)