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
# @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
# @version 1.0
import json, requests
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import redirect
from django.http import JsonResponse
from django.url import reverse_lazy
from django.views.generic import FormView, TemplateView
from base.functions import cargar_consultas, cargar_consulta_id, validar_participacion_general
from .models import RespuestaAbierta, RespuestaOpciones, RespuestaSino 

class ParticipacionIndex(LoginRequiredMixin,TemplateView):
    """!
    Clase que gestiona la vista principal de la participación

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 22-09-2017
    @version 1.0.0
    """
    template_name = "participacion.index.html"
    paginate_by = 5
    
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
        paginator = Paginator(kwargs['consultas'], self.paginate_by)
        page = self.request.GET.get('page')
        try:
            kwargs['page_obj'] = paginator.page(page)
            kwargs['consultas'] = kwargs['page_obj'].object_list
        except PageNotAnInteger:
            kwargs['page_obj'] = paginator.page(1)
            kwargs['consultas'] = kwargs['page_obj'].object_list
        except EmptyPage:
            kwargs['page_obj'] = paginator.page(paginator.num_pages)
            kwargs['consultas'] = kwargs['page_obj'].object_list
        return super(ParticipacionIndex, self).get_context_data(**kwargs)
        

class ParticipacionCreate(LoginRequiredMixin,TemplateView):
    """!
    Clase que gestiona la vista principal de la participación

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 22-02-2017
    @version 1.0.0
    """
    template_name = "participacion.create.html"
    
    def dispatch(self, request, *args, **kwargs):
        """
        Método que redirecciona al usuario si ya paticipó en la consulta
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 24-04-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param request <b>{object}</b> Objeto que contiene la petición
        @param args <b>{object}</b> Objeto que contiene los argumentos
        @param kwargs <b>{object}</b> Objeto que contiene los datos de contexto
        @return Direcciona las encuestas
        """
        if(validar_participacion_general(self.request,int(self.kwargs['pk']))):
            messages.info(self.request,"Ya participó en esta consulta")
            return redirect('participacion_index')
        return super(ParticipacionCreate, self).dispatch(request, *args, **kwargs)
    
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
                elif pregunta['tipo_pregunta']['tipo'] == 'Si/No' or pregunta['tipo_pregunta']['tipo'] == 'Si/No (Justificar No)':
                    if(pregunta['tipo_pregunta']['tipo'] == 'Si/No'):
                        campo += '<p><input type="radio" name="consulta_respuesta_sino_'+str(pregunta['id'])+'" id="'+str(pregunta['id'])+'_1" value="Si">'
                        campo += '<label for="'+str(pregunta['id'])+'_1">Sí</label></p>'
                        campo += '<p><input type="radio" name="consulta_respuesta_sino_'+str(pregunta['id'])+'" id="'+str(pregunta['id'])+'_2" value="No">'
                        campo += '<label for="'+str(pregunta['id'])+'_2">No</label></p>'
                    else:
                        campo += '<p><input type="radio" name="consulta_respuesta_sino_'+str(pregunta['id'])+'" id="'+str(pregunta['id'])+'_1" value="Si" '
                        campo += 'class="need_justification" onclick=show_justification(this,true)>'
                        campo += '<label for="'+str(pregunta['id'])+'_1">Sí</label></p>'
                        campo += '<p><input type="radio" name="consulta_respuesta_sino_'+str(pregunta['id'])+'" id="'+str(pregunta['id'])+'_2" value="No" onclick=show_justification(this,false)>'
                        campo += '<label for="'+str(pregunta['id'])+'_2">No</label></p>'
                        campo += '<div id="div_justificar_'+str(pregunta['id'])+'" style="display:none;">'
                        campo += '<textarea class="form-control" id="respuesta_justificar_'+str(pregunta['id'])+'" name="consulta_respuesta_justificar_'+str(pregunta['id'])+'">'
                        campo += '</textarea></div>'
                else:
                    campo += '<label>La propuesta debe tener entre 10 y 50 caracteres</label><br>'
                    campo += '<div class="input-field"><textarea class="form-control" name="consulta_respuesta_abierta_'+str(pregunta['id'])+'"'
                    campo += 'oninput="medir_caracters(this);quitar_espacios(this);"></textarea>'
                    campo += '<p class="right" id="longitud"><span>0</span> caracteres escritos</p></div><br/><br/><br/>'
                valores[pregunta['id']] = {'label':label,'field':campo}
            kwargs['preguntas'] = valores
        return super(ParticipacionCreate, self).get_context_data(**kwargs)
    
    def post(self,request,pk):
        """!
        Metodo que sobreescribe el post del formulario
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 20-03-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param request <b>{object}</b> Objeto que instancia la petición
        @param pk <b>{int}</b> Recibe el id de la consulta
        @return Retorna los datos de contexto
        """
        data = dict(request.POST)
        del data['csrfmiddlewaretoken']
        if self.request.is_ajax():
            for key in data.keys():
                pregunta_id = key.split("_")[-1]
                if 'sino' in key:
                    value = True if data[key][0] == 'Si' else False
                    justify_id = 'consulta_respuesta_justificar_'+str(pk)
                    self.crear_respuesta_sino(pk,value,pregunta_id,self.request.user.id)
                    if(not value and justify_id in data.keys()):
                        respuesta = data[justify_id][0]
                        self.crear_respuesta_abierta(pk,respuesta,pregunta_id,self.request.user.id,True)
                elif 'radio' in key or 'check' in key:
                    for value in data[key]:
                        self.crear_respuesta_opciones(pk,value,pregunta_id,self.request.user.id)
                elif 'abierta' in key:
                    value = data[key][0]
                    self.crear_respuesta_abierta(pk,value,pregunta_id,self.request.user.id)
            return JsonResponse({"code":True})
        return redirect(reverse_lazy('participacion_busqueda',kwargs={'pk':pk}))
    
    def crear_respuesta_sino(self,consulta_id,value,pregunta_id,user_id):
        """!
        Metodo para crear una respuesta de si/no
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 27-03-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param consulta_id <b>{int}</b> Recibe el número de la consulta
        @param value <b>{bool}</b> Recibe el valor de la respuesta
        @param pregunta_id <b>{int}</b> Recibe el número de la pregunta
        @param user_id <b>{int}</b> Recibe el id del user
        @return Retorna los datos de contexto
        """
        user = User.objects.get(id=user_id)
        respuesta = RespuestaSino()
        respuesta.consulta = consulta_id
        respuesta.pregunta = pregunta_id
        respuesta.respuesta = value
        respuesta.user = user
        respuesta.save()
        
    def crear_respuesta_opciones(self,consulta_id,value,pregunta_id,user_id):
        """!
        Metodo para crear una respuesta de selección simple y múltiple
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 28-03-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param consulta_id <b>{int}</b> Recibe el número de la consulta
        @param value <b>{bool}</b> Recibe el valor de la respuesta
        @param pregunta_id <b>{int}</b> Recibe el número de la pregunta
        @param user_id <b>{int}</b> Recibe el id del user
        @return Retorna los datos de contexto
        """
        user = User.objects.get(id=user_id)
        respuesta = RespuestaOpciones()
        respuesta.consulta = consulta_id
        respuesta.pregunta = pregunta_id
        respuesta.opcion = value
        respuesta.user = user
        respuesta.save()
        
    def crear_respuesta_abierta(self,consulta_id,value,pregunta_id,user_id,es_justificacion = False):
        """!
        Metodo para crear una respuesta abierta
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 28-03-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param consulta_id <b>{int}</b> Recibe el número de la consulta
        @param value <b>{bool}</b> Recibe el valor de la respuesta
        @param pregunta_id <b>{int}</b> Recibe el número de la pregunta
        @param user_id <b>{int}</b> Recibe el id del user
        @param es_justificacion <b>{bool}</b> Recibe el párametro que indica si es una justifiación
        @return Retorna los datos de contexto
        """
        user = User.objects.get(id=user_id)
        respuesta = RespuestaAbierta()
        respuesta.consulta = consulta_id
        respuesta.pregunta = pregunta_id
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
    consulta = request.GET.get('consulta', None)
    if(consulta):
        if(validar_participacion_general(request,consulta)):
            return JsonResponse({'mensaje': True,'participacion':True})
        return JsonResponse({'mensaje': True,'participacion':False})
    else:
        return JsonResponse({'mensaje': False, 'error': str('No envío el id de la consulta')})
    
    
class MiParticipacion(LoginRequiredMixin,TemplateView):
    """!
    Clase para mostrar los resultados en las consultas participadas

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 28-09-2017
    @version 1.0.0
    """
    template_name = "mi_participacion.html"
    paginate_by = 5
    
    def get_context_data(self, **kwargs):
        """!
        Metodo para cargar/obtener valores en el contexto de la vista
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 28-09-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param kwargs <b>{object}</b> Objeto que contiene los datos de contexto
        @return Retorna los datos de contexto
        """
        context = super(MiParticipacion, self).get_context_data(**kwargs)
        consultas = cargar_consultas()
                
        context['object_list'] = self.tomar_participaciones(self.request.user.id,consultas)
        
        ## Implementación del paginador
        paginator = Paginator(context['object_list'], self.paginate_by)
        page = self.request.GET.get('page')
        try:
            context['page_obj'] = paginator.page(page)
            context['object_list'] = context['page_obj'].object_list
        except PageNotAnInteger:
            context['page_obj'] = paginator.page(1)
            context['object_list'] = context['page_obj'].object_list
        except EmptyPage:
            context['page_obj'] = paginator.page(paginator.num_pages)
            context['object_list'] = context['page_obj'].object_list
        return context
    
    def tomar_participaciones(self,user,consultas):
        """!
        Metodo para obtener las participaciones del usuario
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 03-10-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param user <b>{int}</b> Recibe el id del usuario
        @param consultas <b>{dict}</b> Recibe un diccionario con las consultas disponibles
        @return Retorna los datos de contexto
        """
        consulta_user = []
        for consulta in consultas:
            participo = False
            preguntas = []
            for pregunta in consulta['preguntas']:
                preguntas_data = {}
                if(pregunta['tipo_pregunta']['tipo']=="Si/No"):
                    respuesta_sino = RespuestaSino.objects.filter(pregunta=int(pregunta['id']),user_id=user).all()
                    if respuesta_sino:
                        participo = True
                        preguntas_data['texto_pregunta'] = pregunta['texto_pregunta']
                        preguntas_data['tipo_pregunta'] = pregunta['tipo_pregunta']['tipo']
                        preguntas_data['respuestas'] = [resp.respuesta for resp in respuesta_sino]
                elif(pregunta['tipo_pregunta']['tipo']=="Selección Simple" or pregunta['tipo_pregunta']['tipo']=="Selección Múltiple"):
                    respuesta_opciones = RespuestaOpciones.objects.filter(pregunta=int(pregunta['id']),user_id=user).all()
                    if respuesta_opciones:
                        participo = True    
                        preguntas_data['texto_pregunta'] = pregunta['texto_pregunta']
                        preguntas_data['tipo_pregunta'] = pregunta['tipo_pregunta']['tipo']
                        respuestas = []
                        for resp in respuesta_opciones:
                            for opcion in pregunta['opciones']:
                                if(int(opcion['id'])==resp.opcion):
                                    respuestas.append(opcion['texto_opcion'])
                        preguntas_data['respuestas'] = respuestas
                elif(pregunta['tipo_pregunta']['tipo']=="Abierta"):
                    respuesta_abierta = RespuestaAbierta.objects.filter(pregunta=int(pregunta['id']),user_id=user).all()
                    if respuesta_abierta:
                        participo = True
                        preguntas_data['texto_pregunta'] = pregunta['texto_pregunta']
                        preguntas_data['tipo_pregunta'] = pregunta['tipo_pregunta']['tipo']
                        preguntas_data['respuestas'] = [resp.texto_respuesta for resp in respuesta_abierta]
                if(participo):
                    preguntas.append(preguntas_data)        
            if(participo):
                consulta_obj = {}
                consulta_obj['nombre_consulta'] = consulta['nombre_consulta']
                consulta_obj['preguntas'] = preguntas
                consulta_user.append(consulta_obj)
        return consulta_user