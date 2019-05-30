# -*- coding: utf-8 -*-
"""
Sistema de Consulta Pública

Copyleft (@) 2017 CENDITEL nodo Mérida - https://planificacion.cenditel.gob.ve/trac/wiki/ModeladoTopicos_2017
"""
## @package consulta.models
#
# Modelos correspondientes a la aplicación consulta
# @author Rodrigo Boet (rboet at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
# @version 1.0
from __future__ import unicode_literals
from django.contrib.auth.models import User

from django.db import models

class RespuestaSino(models.Model):
    """!
    Clase que gestiona las respuestas con si/no

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 27-03-2017
    @version 1.0.0
    """
    ## Relación con la pregunta
    pregunta = models.IntegerField()
    
    ## Respuesta
    respuesta = models.BooleanField()
    
    ## Relación con el user
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    
    ## Relación con la consulta
    consulta = models.IntegerField()
    
    def __str__(self):
        """!
        Metodo que sobreescribir la presentación de datos en la aplicación
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 28-09-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Retorna el objeto en str
        """
        return self.user.username+" - "+ "Si" if self.respuesta else "No" + str(self.consulta)

class RespuestaOpciones(models.Model):
    """!
    Clase que gestiona las respuestas con opciones

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 27-03-2017
    @version 1.0.0
    """
    ## Relación con la pregunta
    pregunta = models.IntegerField()
    
    ## Relación con la opción de la respuesta
    opcion = models.IntegerField()
    
    ## Relación con el user
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    
    ## Relación con la consulta
    consulta = models.IntegerField()
    
    def __str__(self):
        """!
        Metodo que sobreescribir la presentación de datos en la aplicación
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 28-09-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Retorna el objeto en str
        """
        return self.user.username+" - "+ str(self.consulta)
    
class RespuestaAbierta(models.Model):
    """!
    Clase que gestiona las respuestas abiertas y con justifiación

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 27-03-2017
    @version 1.0.0
    """
    ## Texto de la respuesta
    texto_respuesta = models.TextField()
    
    ## Relación con la pregunta
    pregunta = models.IntegerField()
    
    ## Relación con la consulta
    consulta = models.IntegerField()
    
    ## Si la pregunta es de justificación
    es_justificacion = models.BooleanField(default=False)
    
    ## Relación con el user
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    
    def __str__(self):
        """!
        Metodo que sobreescribir la presentación de datos en la aplicación
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 28-09-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Retorna el objeto en str
        """
        return self.user.username + " - " + str(self.consulta)
    
