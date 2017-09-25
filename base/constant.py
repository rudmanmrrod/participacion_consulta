# -*- coding: utf-8 -*-
"""
Sistema de Consulta Pública

Copyleft (@) 2017 CENDITEL nodo Mérida - https://planificacion.cenditel.gob.ve/trac/wiki/ModeladoTopicos_2017
"""
## @package base.constant
#
# Contiene las constantes del sistema de consulta pública
# @author Rodrigo Boet (rboet at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
# @version 1.0
from __future__ import unicode_literals

## Nacionalidades (ABREVIADO)
SHORT_NACIONALIDAD = (
    ("V", "V"), ("E", "E")
)

## Sectores
SECTORES = (
    ('TR','Trabajadores'),
    ('CP','Campesinos y pescadores'),
    ('ES','Estudiantes'),
    ('PD','Personas con alguna discapacidad'),
    ('PI','Pueblos indígenas'),
    ('PE','Pensionados'),
    ('EM','Empresarios'),
    ('CM','Comunas y Consejos Comunales'),    
)

## Sector Trabajador
SECTOR_TRABAJADOR = (
    ('PT','Petróleo'),
    ('MI','Minería'),
    ('IB','Industrias básicas'),
    ('ED','Educación'),
    ('SA','Salud'),
    ('DE','Deporte'),
    ('TR','Transporte'),
    ('CS','Construcción'),
    ('CL','Cultores'),
    ('IT','Intelectuales'),
    ('PR','Prensa'),
    ('CT','Ciencia y Tecnología'),
    ('AP','Administración Pública'),
)

## Sector Estudiante
SECTOR_ESTUDIANTE = (
    ('Upu','Educación universitaria pública'),
    ('Upr','Educación universitaria privada'),
    ('MEd','Misiones educativas'),
)

## Tipo de participacion
PARTICIPACION = (
    ('IN','Individual'),
    ('CO','Colectiva'),
)

## Tipo de Institución
TIPO_INSTITUCION = (
    ('Upr','Universidad Privada'),
    ('Upl','Universidad Publica'),
    ('Mis','Misión')
)

## Objetivos prágmaticos de la constituyente

OBJETIVOS = (
    (1,("La Paz como necesidad, derecho y anhelo de la Nación")),
    (2,("El perfeccionamiento del sistema económico nacional hacia la Venezuela Potencia")),
    (3,("Constitucionalizar las Misiones y Grandes Misiones Socialistas")),
    (4,("La ampliación de las competencias del sistema de Justicia, para erradicar la impunidad de los delitos")),
    (5,("Constitucionalización de las nuevas formas de Democracia Participativa y Protagónica")),
    (6,("La defensa de la soberanía y la integridad de la Nación y protección contra el intervencionismo extranjero")),
    (7,("Reivindicación del carácter pluricultural de la Patria")),
    (8,("La garantía del futuro")),
    (9,("La preservación de la vida en el planeta")),
)

OBJETIVOS_DICT = {
    1:"La Paz como necesidad, derecho y anhelo de la Nación",
    2:"El perfeccionamiento del sistema económico nacional hacia la Venezuela Potencia",
    3:"Constitucionalizar las Misiones y Grandes Misiones Socialistas",
    4:"La ampliación de las competencias del sistema de Justicia, para erradicar la impunidad de los delitos",
    5:"Constitucionalización de las nuevas formas de Democracia Participativa y Protagónica",
    6:"La defensa de la soberanía y la integridad de la Nación y protección contra el intervencionismo extranjero",
    7:"Reivindicación del carácter pluricultural de la Patria",
    8:"La garantía del futuro",
    9:"La preservación de la vida en el planeta",
}

## Definición de los objetivos
OBJETIVOS_DEFINICION = (
    (1,("""La Paz como necesidad, derecho y anhelo de la Nación, el proceso constituyente es una gran convocatoria a un diálogo nacional para contener la
        escalada de la violencia política, mediante el reconocimiento político mutuo y de una reorganización del Estado, que recupere el principio constitucional
        de cooperación entre los poderes públicos, como garantía del pleno funcionamiento del Estado democrático, social, de derecho y de justicia, superando
        el actual clima de impunidad.""")),
    (2,("""El perfeccionamiento del sistema económico nacional hacia la Venezuela Potencia, concebir el nuevo modelo de la economía post petrolera, mixta,
        productiva, diversificada, integradora, a partir de la creación de nuevos instrumentos que dinamicen el desarrollo de las fuerzas productivas,
        así como la instauración de un nuevo modelo de distribución transparente que satisfaga plenamente las necesidades de abastecimiento de la población.""")),
    (3,("""Constitucionalizar las Misiones y Grandes Misiones Socialistas, desarrollando el Estado democrático, social, de derecho y de justicia, hacia un
        Estado de la Suprema Felicidad Social, con el fin de preservar y ampliar el legado del Comandante Hugo Chávez, en materia del pleno goce y ejercicio
        de los derechos sociales para nuestro pueblo.""")),
    (4,("""La ampliación de las competencias del sistema de Justicia, para erradicar la impunidad de los delitos, especialmente aquellos que se cometen
        contra las personas (homicidios, secuestro, extorsión, violaciones, violencia de género y contra los niños y niñas); así como de los delitos contra
        la Patria y la sociedad tales como la corrupción; el contrabando de extracción; la especulación; el terrorismo; el narcotráfico; la promoción del odio
        social y la injerencia extranjera.""")),
    (5,("""Constitucionalización de las nuevas formas de Democracia Participativa y Protagónica, a partir del reconocimiento de los nuevos sujetos del
        Poder Popular, tales como las Comunas y Consejos Comunales, Consejos de Trabajadores y Trabajadoras, entre otras formas de organización de base
        territorial y social de la población.""")),
    (6,("""La defensa de la soberanía y la integridad de la Nación y protección contra el intervencionismo extranjero, ampliando las competencias
        del Estado democrático, social, de derecho y de justicia para la preservación de la sseguridad ciudadana, la garantía del ejercicio integral de los
        derechos humanos, la defensa de la independencia, la paz, la inmunidad, y la soberanía política, económica y territorial de Venezuela. Asi como la
        promoción de la consolidación de un mundo pluripolar y multicéntrico que garantice el respeto al derecho y a la seguridad internacional.""")),
    (7,("""Reivindicación del carácter pluricultural de la Patria, mediante el desarrollo constitucional de los valores espirituales que nos permitan
        reconocernos como venezolanos y venezolanas, en nuestra diversidad étnica y cultural como garantía de convivencia pacífica en el presente
        y hacia el porvenir, vacunándonos contra el odio social y racial incubado en una minoría de la sociedad.""")),
    (8,("""La garantía del futuro, nuestra juventud , mediante la inclusión de un capítulo constitucional para consagrar los derechos de la juventud,
        tales como el uso libre y consciente de las tecnologías de información; el derecho a un trabajo digno y liberador de sus creatividades;
        la protección a las madres jóvenes; el acceso a una primera vivienda; y el reconocimiento a la diversidad de sus gustos, estilos
        y pensamientos, entre otros.""")),
    (9,("""La preservación de la vida en el planeta, desarrollando constitucionalmente, con mayor especificidad los derechos soberanos sobre
        la protección de nuestra biodiversidad y el desarrollo de una cultura ecológica en nuestra sociedad.""")),
)