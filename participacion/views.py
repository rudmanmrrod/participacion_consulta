# -*- coding: utf-8 -*-
"""
Sistema de Participación en Consultas

Copyleft (@) 2017 CENDITEL nodo Mérida - https://planificacion.cenditel.gob.ve/trac/wiki/ModeladoTopicos_2017
"""
## @package participacion.views
#
# Vistas correspondientes a la aplicación participacion
# @author Rodrigo Boet (rboet at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
# @version 1.0
import json
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy
from django.http import JsonResponse
from django.views.generic import FormView, TemplateView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from base.functions import cargar_consultas, cargar_consulta_id
from .models import RespuestaAbierta, RespuestaOpciones, RespuestaSino
import requests

class ParticipacionIndex(TemplateView):
    """!
    Clase que gestiona la vista principal de la participación

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 22-09-2017
    @version 1.0.0
    """
    template_name = "participacion.index.html"
    
    def get_context_data(self, **kwargs):
        """!
        Metodo que permite cargar de nuevo valores en los datos de contexto de la vista
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 22-09-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param kwargs <b>{object}</b> Objeto que contiene los datos de contexto
        @return Retorna los datos de contexto
        """
        kwargs['consultas'] = cargar_consultas()
        return super(ParticipacionIndex, self).get_context_data(**kwargs)
        

class ParticipacionCreate(TemplateView):
    """!
    Clase que gestiona la vista principal de la participación

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 22-02-2017
    @version 1.0.0
    """
    template_name = "participacion.create.html"
    
    def get_context_data(self, **kwargs):
        """!
        Metodo que permite cargar de nuevo valores en los datos de contexto de la vista
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 23-02-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param kwargs <b>{object}</b> Objeto que contiene los datos de contexto
        @return Retorna los datos de contexto
        """
        valores = {}
        consulta = cargar_consulta_id(kwargs['pk'])
        if consulta:
            for pregunta in consulta['preguntas']:
                label = '<label class="center">'+pregunta['texto_pregunta']+'</label>'
                campo = ''
                print(pregunta)
                if pregunta['tipo_pregunta']['tipo'] == 'Selección Simple':
                    campo = ''
                    for opcion in pregunta['opciones']:
                        campo += '<p><input type="radio" name="consulta_respuesta_radio_'+str(pregunta['id'])+'" id="'+str(opcion['id'])+'"value="'+str(opcion['id'])+'">'
                        campo += '<label for="'+str(opcion['id'])+'">'+opcion['texto_opcion']+'</label></p>'
                elif pregunta['tipo_pregunta']['tipo'] == 'Selección Múltiple':
                    campo = ''
                    for opcion in pregunta['opciones']:
                        campo += '<p><input type="checkbox" name="consulta_respuesta_check_'+str(pregunta['id'])+'" id="'+str(opcion['id'])+'"value="'+str(opcion['id'])+'">'
                        campo += '<label for="'+str(opcion['id'])+'">'+opcion['texto_opcion']+'</label></p>'
                elif pregunta['tipo_pregunta']['tipo'] == 'Si/No' and pregunta['tipo_pregunta']['tipo'] == 'Si/No (Justificar No)':
                    if(pregunta['tipo_pregunta']['tipo'] == 'Si/No'):
                        campo += '<p><input type="radio" name="consulta_respuesta_sino_'+str(pregunta['id'])+'" id="'+str(opcion['id'])+'"value="Si">'
                        campo += '<label for="'+str(opcion['id'])+'">Sí</label></p>'
                        campo += '<p><input type="radio" name="consulta_respuesta_sino_'+str(pregunta['id'])+'" id="'+str(opcion['id'])+'"value="No">'
                        campo += '<label for="'+str(opcion['id'])+'">No</label></p>'
                    else:
                        campo += '<p><input type="radio" name="consulta_respuesta_sino_'+str(pregunta['id'])+'" id="'+str(opcion['id'])+'"value="Si" class="need_justification">'
                        campo += '<label for="'+str(opcion['id'])+'">Sí</label></p>'
                        campo += '<p><input type="radio" name="consulta_respuesta_sino_'+str(pregunta['id'])+'" id="'+str(opcion['id'])+'"value="No">'
                        campo += '<label for="'+str(opcion['id'])+'">No</label></p>'
                        campo += '<div id="div_justificar_'+kwargs['pk']+'" style="display:none;"><label>Indique con que instrumento legal en vigencia se relaciona su aporte</label>'
                        campo += '<textarea class="form-control" id="respuesta_justificar_'+kwargs['pk']+'" name="consulta_respuesta_justificar_'+str(pregunta['id'])+'">'
                        campo += '</textarea></div>'
                else:
                    campo += '<label class="text-center">La propuesta debe tener entre 700 y 5000 caracteres</label><br>'
                    campo += '<div class="input-field"><textarea class="form-control" name="consulta_respuesta_abierta_'+str(pregunta['id'])+'" oninput="medir_caracters(this);"></textarea></div>'
                    campo += '<p class="right" id="longitud"><span>0</span> caracteres escritos</p><br/><br/><br/>'
                valores[pregunta['id']] = {'label':label,'field':campo}
            kwargs['preguntas'] = valores
        return super(ParticipacionCreate, self).get_context_data(**kwargs)
    
    def post(self,request,pk,id_objetivo):
        """!
        Metodo que sobreescribe el post del formulario
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 20-03-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param request <b>{object}</b> Objeto que instancia la petición
        @param pk <b>{int}</b> Recibe el id de la consulta
        @param id_ente <b>{int}</b> Recibe el id del ente
        @return Retorna los datos de contexto
        """
        data = dict(request.POST)
        del data['csrfmiddlewaretoken']
        if self.request.is_ajax():
            for key in data.keys():
                parent_id = key.split("_")[-1]
                if 'sino' in key:
                    value = True if data[key][0] == 'Si' else False
                    justify_id = 'consulta_respuesta_justificar_'+str(parent_id)
                    self.crear_respuesta_sino(parent_id,value,id_objetivo,self.request.user.id)
                    if(not value and justify_id in data.keys()):
                        respuesta = data[justify_id][0]
                        self.crear_respuesta_abierta(parent_id,respuesta,id_objetivo,self.request.user.id,True)
                elif 'radio' in key or 'check' in key:
                    for value in data[key]:
                        self.crear_respuesta_opciones(value,id_objetivo,self.request.user.id)
                elif 'abierta' in key:
                    value = data[key][0]
                    self.crear_respuesta_abierta(parent_id,value,id_objetivo,self.request.user.id)
            return JsonResponse({"code":True})
        return redirect(reverse_lazy('participacion_busqueda',kwargs={'pk':pk}))
    
    def crear_respuesta_sino(self,pregunta_id,value,user_id):
        """!
        Metodo para crear una respuesta de si/no
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 27-03-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param pregunta_id <b>{int}</b> Recibe el número de la pregunta
        @param value <b>{bool}</b> Recibe el valor de la respuesta
        @param user_id <b>{int}</b> Recibe el id del user
        @return Retorna los datos de contexto
        """
        user = User.objects.get(id=user_id)
        respuesta = RespuestaSino()
        respuesta.pregunta = pregunta_id
        respuesta.respuesta = value
        respuesta.user = user
        respuesta.save()
        
    def crear_respuesta_opciones(self,opcion_id,user_id):
        """!
        Metodo para crear una respuesta de selección simple y múltiple
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 28-03-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param parent_id <b>{int}</b> Recibe el número del id del padre
        @param user_id <b>{int}</b> Recibe el id del user
        @return Retorna los datos de contexto
        """
        user = User.objects.get(id=user_id)
        respuesta = RespuestaOpciones()
        respuesta.opcion = opcion_id
        respuesta.user = user
        respuesta.save()
        
    def crear_respuesta_abierta(self,pregunta_id,value,user_id,es_justificacion = False):
        """!
        Metodo para crear una respuesta abierta
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 28-03-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param pregunta_id <b>{int}</b> Recibe el número del id de la pregunta
        @param value <b>{str}</b> Recibe el valor de la respuesta
        @param user_id <b>{int}</b> Recibe el id del user
        @param es_justificacion <b>{bool}</b> Recibe el párametro que indica si es una justifiación
        @return Retorna los datos de contexto
        """
        user = User.objects.get(id=user_id)
        respuesta = RespuestaAbierta()
        respuesta.pregunta = pregunta_id
        respuesta.objetivo = id_objetivo
        respuesta.texto_respuesta = value
        respuesta.user = user
        respuesta.es_justificacion = es_justificacion
        respuesta.save()


def validar_participacion(request):
    """!
    Función que valida si un usuario ya participó en la consulta con un ente en particular

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright GNU/GPLv2
    @date 21-04-2017
    @param request <b>{object}</b> Objeto que contiene la petición
    @return Retorna un json con la respuesta
    """
    if not request.is_ajax():
        return JsonResponse({'mensaje': False, 'error': str('La solicitud no es ajax')})
    pregunta = request.GET.get('pregunta', None)
    if(pregunta):
        respuesta_sino = RespuestaSino.objects.filter(user_id=request.user.id,pregunta=pregunta)
        respuesta_abierta = RespuestaAbierta.objects.filter(user_id=request.user.id,pregunta=pregunta,)
        respuesta_opciones = RespuestaOpciones.objects.filter(user_id=request.user.id,pregunta=pregunta)
        if(respuesta_sino or respuesta_abierta or respuesta_opciones):
            return JsonResponse({'mensaje': True,'participacion':True})
        return JsonResponse({'mensaje': True,'participacion':False})
    else:
        return JsonResponse({'mensaje': False, 'error': str('No envío el id de la pregunta')})
    
    
    
class ParticipacionSimpleCreate(LoginRequiredMixin,TemplateView):
    """!
    Clase que gestiona la vista principal de la participación simple

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 18-07-2017
    @version 1.0.0
    """
    template_name = "participacion.create.simple.html"
    
    def get_context_data(self, **kwargs):
        """!
        Metodo que permite cargar de nuevo valores en los datos de contexto de la vista
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 23-02-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param kwargs <b>{object}</b> Objeto que contiene los datos de contexto
        @return Retorna los datos de contexto
        """
        valores = {}
        for pregunta in Pregunta.objects.filter(consulta_id=kwargs['pk']).all():
            label = '<label class="text-center">'+pregunta.texto_pregunta+'</label>'
            campo = ''
            if pregunta.tipo_pregunta.id == 1:
                campo = ''
                for opcion in Opcion.objects.filter(pregunta_id=pregunta.id).all():
                    campo += '<label for="'+kwargs['pk']+'">'+opcion.texto_opcion+'</label><input type="radio" name="consulta_respuesta_radio_'+str(pregunta.id)+'" id="'+kwargs['pk']+'"value="'+str(opcion.id)+'" class="icheck">'
            elif pregunta.tipo_pregunta.id == 2:
                campo = ''
                for opcion in Opcion.objects.filter(pregunta_id=pregunta.id).all():
                    campo += '<label for="'+kwargs['pk']+'">'+opcion.texto_opcion+'</label><input type="checkbox" name="consulta_respuesta_check_'+kwargs['pk']+'" id="'+kwargs['pk']+'"value="'+str(opcion.id)+'" class="icheck">'
            elif pregunta.tipo_pregunta.id > 2 and pregunta.tipo_pregunta.id < 5:
                if(pregunta.tipo_pregunta.id == 3):
                    campo += '<label for="'+kwargs['pk']+'">Si</label><input type="radio" name="consulta_respuesta_sino_'+str(pregunta.id)+'" id="'+kwargs['pk']+'"value="Si" class="icheck">'
                    campo += '<label for="'+kwargs['pk']+'">No</label><input type="radio" name="consulta_respuesta_sino_'+str(pregunta.id)+'" id="'+kwargs['pk']+'"value="No" class="icheck">'
                else:
                    campo += '<label for="'+kwargs['pk']+'">Si</label><input type="radio" name="consulta_respuesta_sino_'+str(pregunta.id)+'" id="'+kwargs['pk']+'"value="Si" class="icheck need_justification">'
                    campo += '<label for="'+kwargs['pk']+'">No</label><input type="radio" name="consulta_respuesta_sino_'+str(pregunta.id)+'" id="'+kwargs['pk']+'"value="No" class="icheck">'
                    campo += '<div id="div_justificar_'+kwargs['pk']+'" style="display:none;"><label>Indique con que instrumento legal en vigencia se relaciona su aporte</label>'
                    campo += '<textarea class="form-control" id="respuesta_justificar_'+kwargs['pk']+'" name="consulta_respuesta_justificar_'+str(pregunta.id)+'">'
                    campo += '</textarea></div>'
            valores[pregunta.id] = {'label':label,'field':campo}
            kwargs['preguntas'] = valores
        return super(ParticipacionSimpleCreate, self).get_context_data(**kwargs)
    
    def post(self,request,pk,id_objetivo):
        """!
        Metodo que sobreescribe el post del formulario
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 20-03-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param request <b>{object}</b> Objeto que instancia la petición
        @param pk <b>{int}</b> Recibe el id de la consulta
        @param id_ente <b>{int}</b> Recibe el id del ente
        @return Retorna los datos de contexto
        """
        data = dict(request.POST)
        del data['csrfmiddlewaretoken']
        if self.request.is_ajax():
            for key in data.keys():
                parent_id = key.split("_")[-1]
                if 'sino' in key:
                    value = True if data[key][0] == 'Si' else False
                    justify_id = 'consulta_respuesta_justificar_'+str(parent_id)
                    self.crear_respuesta_sino(parent_id,value,id_objetivo,self.request.user.id)
                    if(not value and justify_id in data.keys()):
                        respuesta = data[justify_id][0]
                        self.crear_respuesta_abierta(parent_id,respuesta,id_objetivo,self.request.user.id,True)
                elif 'radio' in key or 'check' in key:
                    for value in data[key]:
                        self.crear_respuesta_opciones(value,id_objetivo,self.request.user.id)
            return JsonResponse({"code":True})
        return redirect(reverse_lazy('participacion_busqueda',kwargs={'pk':pk}))
    
    def crear_respuesta_sino(self,parent_id,value,id_objetivo,user_id):
        """!
        Metodo para crear una respuesta de si/no
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 27-03-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param parent_id <b>{int}</b> Recibe el número del id del padre
        @param value <b>{bool}</b> Recibe el valor de la respuesta
        @param id_objetivo <b>{int}</b> Recibe el id del objetivo
        @param user_id <b>{int}</b> Recibe el id del user
        @return Retorna los datos de contexto
        """
        user = User.objects.get(id=user_id)
        parent = Pregunta.objects.get(pk=parent_id)
        respuesta = RespuestaSino()
        respuesta.pregunta = parent
        respuesta.respuesta = value
        respuesta.user = user
        respuesta.save()
        
    def crear_respuesta_opciones(self,parent_id,id_objetivo,user_id):
        """!
        Metodo para crear una respuesta de selección simple y múltiple
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 28-03-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param parent_id <b>{int}</b> Recibe el número del id del padre
        @param id_objetivo <b>{int}</b> Recibe el id del objetivo
        @param user_id <b>{int}</b> Recibe el id del user
        @return Retorna los datos de contexto
        """
        user = User.objects.get(id=user_id)
        parent = Opcion.objects.get(pk=parent_id)
        respuesta = RespuestaOpciones()
        respuesta.opcion = parent
        respuesta.user = user
        respuesta.save()