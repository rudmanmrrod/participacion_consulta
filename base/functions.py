# -*- coding: utf-8 -*-
"""
Sistema de Participación en Consultas

Copyleft (@) 2017 CENDITEL nodo Mérida - https://planificacion.cenditel.gob.ve/trac/wiki/ModeladoTopicos_2017
"""
## @package base.functions
#
# Clases genéricas de la consulta
# @author Rodrigo Boet (rboet at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
# @version 1.0
from __future__ import unicode_literals
from django.contrib.auth.models import User
from participacion.models import RespuestaAbierta
from participacion_consulta.settings import API_URL, CONSULTA_SECRET_TOKEN
import requests

def cargar_tipo_pregunta():
    """!
    Función que permite cargar los tipos de preguntas que existen

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 15-02-2017
    @return Devuelve una tupla con los tipos de pregunta
    """

    lista = ('', 'Seleccione...'),

    try:
        for tipo_pregunta in TipoPregunta.objects.all():
            lista += (tipo_pregunta.id, tipo_pregunta.tipo),
    except Exception as e:
        pass

    return lista

def cargar_entidad():
    """!
    Función que permite cargar todas las entidades

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 20-04-2017
    @return Devuelve una tupla con las entidades
    """

    lista = ('', 'Seleccione...'),

    try:
        for entidad in Entidad.objects.all():
            lista += (entidad.codigo, entidad.nombre),
    except Exception as e:
        pass

    return lista


def cargar_municipios():
    """!
    Función que permite cargar todas los municipios

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 20-04-2017
    @return Devuelve una tupla con los municipios
    """

    lista = ('', 'Seleccione...'),

    try:
        for municipio in Municipio.objects.all():
            lista += (municipio.codigo, municipio.nombre),
    except Exception as e:
        pass

    return lista


def cargar_parroquias():
    """!
    Función que permite cargar todas las parroquias

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 20-04-2017
    @return Devuelve una tupla con las parroquias
    """

    lista = ('', 'Seleccione...'),

    try:
        for parroquia in Parroquia.objects.all():
            lista += (parroquia.codigo, parroquia.nombre),
    except Exception as e:
        pass

    return lista


def validate_cedula(cedula):
    """!
    Función que permite validar la cedula

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 20-04-2017
    @param cedula {str} Recibe el número de cédula
    @return Devuelve verdadero o falso
    """
    
    cedula = Perfil.objects.filter(cedula=cedula)
    if cedula:
        return True
    else:
        return False
    
def validate_email(email):
    """!
    Función que permite validar la cedula

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 20-04-2017
    @param cedula {str} Recibe el número de cédula
    @return Devuelve verdadero o falso
    """
    
    email = User.objects.filter(email=email)
    if email:
        return True
    else:
        return False

def cargar_preguntas(id):
    """!
    Función que permite cargar preguntas asignadas a una consulta

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 31-05-2017
    @return Devuelve una tupla con las consultas
    """

    lista = ('', 'Seleccione...'),

    try:
        for pregunta in Pregunta.objects.filter(consulta_id=id).all():
            lista += (pregunta.id, pregunta.texto_pregunta),
    except Exception as e:
        pass

    return lista

def load_consult(token):
    """!
    Función que permite cargar las consultas configuradas en el settings

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @token str Recibe el token de la consulta
    @date 22-09-2017
    @return Devuelve una tupla con las consultas
    """
    r = requests.get(API_URL+'consulta/'+token)
    if not r.status_code == 200:
        return False
    data = r.json()[0]
    return data

def cargar_consultas():
    """!
    Función que permite cargar las consultas configuradas en el settings

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 22-09-2017
    @return Devuelve una tupla con las consultas
    """
    if type(CONSULTA_SECRET_TOKEN) == str:
        return load_consult(item)
    elif type(CONSULTA_SECRET_TOKEN) == list:
        data = []
        for item in CONSULTA_SECRET_TOKEN:
            data.append(load_consult(item))
        return data
    else:
        return False
    
def cargar_consulta_id(id):
    """!
    Función que permite cargar las consultas por id

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 22-09-2017
    @return Devuelve una tupla con las consultas
    """
    if type(CONSULTA_SECRET_TOKEN) == str:
        consulta = load_consult(item)
        if (consulta['id']==int(id)):
            return consulta
        else:
            return False
    elif type(CONSULTA_SECRET_TOKEN) == list:
        consulta = False
        for item in CONSULTA_SECRET_TOKEN:
            item = load_consult(item)
            if (item['id']==int(id)):
                consulta = item
        return consulta
    return False
