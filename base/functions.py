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
from django.contrib.auth import authenticate
from participacion.models import RespuestaAbierta,RespuestaOpciones, RespuestaSino
from participacion_consulta.settings import API_BASE_URL,API_URL, CONSULTA_SECRET_TOKEN
import requests


def cargar_entidad():
    """!
    Función que permite cargar todas las entidades

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 20-04-2017
    @return Devuelve una tupla con las entidades
    """

    lista = ('', 'Seleccione...'),

    try:
        entidades = requests.get(API_URL+'entidad/')
        for entidad in entidades.json():
            lista += (entidad['codigo'], entidad['nombre']),
    except Exception as e:
        pass

    return lista


def cargar_municipios(entidad = 0):
    """!
    Función que permite cargar todas los municipios

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 20-04-2017
    @param entidad <b>{int}</b> Recibe el id del padre
    @return Devuelve una tupla con los municipios
    """

    lista = ('', 'Seleccione...'),

    try:
        url = API_URL+'municipio/' if entidad ==0 else API_URL+'municipio/?estado='+str(entidad)
        municipios = requests.get(url)
        for municipio in municipios.json():
            lista += (municipio['codigo'], municipio['nombre']),
    except Exception as e:
        pass

    return lista


def cargar_parroquias(municipio = 0):
    """!
    Función que permite cargar todas las parroquias

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 20-04-2017
    @param municipio <b>{int}</b> Recibe el id del padre
    @return Devuelve una tupla con las parroquias
    """

    lista = ('', 'Seleccione...'),

    try:
        url = API_URL+'parroquia/' if municipio ==0 else API_URL+'parroquia/?municipio='+str(municipio)
        parroquias = requests.get(url)
        for parroquia in parroquias.json():
            lista += (parroquia['codigo'], parroquia['nombre']),
    except Exception as e:
        pass

    return lista


def validate_cedula(cedula):
    """!
    Función que permite validar la cedula

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
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
    @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
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
    @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
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
    @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
    @param token <b>str</b> Recibe el token de la consulta
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
    @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
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
    @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
    @param id <b>int</b> Recibe el id de la consulta
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

def autenticar_rest(username,password):
    """!
    Función que permite autenticarse por rest

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
    @param username <b>str</b> Recibe el nombre de usuario
    @param password <b>str</b> Recibe la contraseña
    @date 28-09-2017
    @return Devuelve los datos del usuario
    """
    r = requests.post(API_BASE_URL+'api-token-auth/',data={"username":username,"password":password})
    if not r.status_code == 200:
        return False
    data = r.json()
    return data

def get_user_data(username,password,token):
    """!
    Función que permite cargar las consultas por id

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
    @param username <b>str</b> Recibe el nombre de usuario
    @param password <b>str</b> Recibe la contraseña
    @param token <b>str</b> Recibe el token de JWT
    @date 28-09-2017
    @return Devuelve los datos del usuario
    """
    header = {'Authorization':'JWT '+token}
    r = requests.get(API_URL+'user/',headers=header)
    if not r.status_code == 200:
        return False
    data = r.json()[0]
    return data

def check_or_create(user_data,password):
    """!
    Función que permite comprobar si el usuario existe de este lado de la aplicación

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
    @param user_data <b>dict</b> Recibe el diccionario con los datos del usuario
    @param password <b>str</b> Recibe la contraseña
    @date 28-09-2017
    @return Devuelve el usuario autenticado
    """
    user =  User.objects.filter(username=user_data["user"]["username"])
    if(user):
        user = user.get()
        user.first_name = user_data['user']['first_name']
        user.last_name = user_data['user']['last_name']
        user.email = user_data['user']['email']
        user.set_password(password)
        user.save()
    else:
        user = User()
        user.username = user_data['user']['username']
        user.first_name = user_data['user']['first_name']
        user.last_name = user_data['user']['last_name']
        user.email = user_data['user']['email']
        user.set_password(password)
        user.save()
    return authenticate(username=user.username, password=password)


def validar_participacion_general(request,consulta_id):
    """!
    Función que permite comprobar si el usuario participó en la consulta

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
    @param request <b>obj</b> Recibe el objeto de la petición
    @param consulta_id <b>int</b> Recibe el id de la consulta
    @date 28-09-2017
    @return Devuelve si el usuario participó o no
    """
    respuesta_sino = RespuestaSino.objects.filter(user_id=request.user.id,consulta=consulta_id)
    respuesta_abierta = RespuestaAbierta.objects.filter(user_id=request.user.id,consulta=consulta_id)
    respuesta_opciones = RespuestaOpciones.objects.filter(user_id=request.user.id,consulta=consulta_id)
    if(respuesta_sino or respuesta_abierta or respuesta_opciones):
        return True
    return False