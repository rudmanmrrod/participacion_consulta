/**
 * Función para agregar preguntas en la consulta
 * @param element Recibe nombre de elemento a agregar
**/
function agregar_preguntas(element) {
    $('#agregar_preguntas').append($(element).html());
}

/**
 * Función para eliminar preguntas agregadas dinámicamente
 * @param element Recibe el elemento a partir del cual se eliminará la fila
**/
function eliminar_preguntas(element) {
    $(element).parent().parent().parent().remove();
}

/**
 * Función para validar las preguntas agregadas dinámicamente
 * @param event Recibe el evento click
**/
function validar_preguntas(event) {
    var longitud = $('#agregar_preguntas').find('.row');
    if(longitud.length>0)
    {
        var vacio = false;
        $.each(longitud.find('input'),function(key,value){
            if ($(value).val().trim()=='') {
                vacio = true;
            }
        });
        $.each(longitud.find('select'),function(key,value){
            if ($(value).val().trim()=='') {
                vacio = true;
            }
        });
        if (vacio) {
            event.preventDefault();
            bootbox.dialog({
                message: "Debe llenar todas las preguntas que agregó",
                title: "<b class='text-danger'>Error</b>",
                buttons: {
                    success: {
                        label: "Cerrar",
                        className: "btn-red",
                        callback: function() {}
                    }
                }
            });
        }
    }
}

/**
 * Función para cargar preguntas luego de un error en el formulario
**/
function cargar_preguntas() {
    $.each(opciones,function(){
        $('#agregar_preguntas').append($('#preguntas').html());    
    });
    $.each($('#agregar_preguntas #id_texto_pregunta_modal'),function(key,value){
        $(value).val(opciones[key]['texto_pregunta']);
    });
    $.each($('#agregar_preguntas #id_tipo_pregunta_modal'),function(key,value){
        $(value).val(opciones[key]['tipo_pregunta']).change();
    });
}

/**
 * Función para agregar opciones si la pregunta lo requiere
 * @param element Recibe el elemento de la consulta
**/
function add_option(element) {
    var option = $(element).parent().parent().parent().find('#for_options');
    $(option).append($('#agregar_opciones').html());
}

/**
 * Función para agregar opciones si la pregunta lo requiere
 * @param element Recibe el id de la consulta
**/
function remove_option(element) {
    $(element).parent().parent().parent().remove();
}

/**
 * Función para mostrar las preguntas de una consulta
 * @param id Recibe el id de la consulta
**/
function ver_preguntas(id) {
    $.ajax({
        type: 'GET',
        url: "/administrador/consulta/ajax/pregunta-list/"+id,
        success: function(response) {
            if (response.success) {
                var preguntas = response.preguntas;
                var token = $('input').val();
                var html = '<form action="" role="form" method="post" id="question_form">';
                html += '<input type="hidden" name="csrfmiddlewaretoken" value="'+token+'">';
                $.each(preguntas,function(key,value){
                    html += "<h4>Pregunta #"+parseInt(key+1)+"</h4>";
                    html+= $('#preguntas').html();
                    html += "<hr>";
                });
                html += "</form>";
                bootbox.dialog({
                    message: html,
                    title: "Preguntas",
                    buttons: {
                        success: {
                            label: "Guardar",
                            className: "btn-primary",
                            callback: function() {
                                update_question();
                            }
                        },
                        close: {
                            label: "Cerrar",
                            className: "btn-red",
                            callback: function() {}
                        }
                    }
                });
                $.each($('.bootbox-body #id_texto_pregunta_modal'),function(key,value){
                    $(value).val(preguntas[key]['texto_pregunta']);
                    $(value).append('<input type="hidden" name="texto_pregunta_id" value="'+preguntas[key]['id']+'">');
                });
                $.each($('.bootbox-body select'),function(key,value){
                    $(value).val(preguntas[key]['tipo_pregunta']).change();
                    if (preguntas[key]['tipo_pregunta']<=2) {
                        var padre = $(value).parent().parent().parent().parent()
                        var agregar_opciones = $(padre).find("#add_options");
                        html = '<h5 class="text-success">Agregar opción '
                        html += '<a href="#" onclick="agregar_opcion('+preguntas[key]['id']+')">';
                        html += '<span class="glyphicon glyphicon-plus text-success"></span></a></h5>';
                        $(agregar_opciones).append(html);
                        html = '<div class="col-sm-12"><h5 class="text-info">Ver opciones '
                        html += '<a href="#" onclick="see_option('+preguntas[key]['id']+')">';
                        html += '<span class="glyphicon glyphicon-plus text-info"></span></a></h5></div>';
                        $(padre).append(html);
                    }
                });
                $.each($('.bootbox-body h4 a'),function(key,value){
                    $(value).attr('onclick','del_pregunta(this,'+preguntas[key]['id']+')');
                });
            }
            else{
                
            }
        },
        error:function(error)
        {
            bootbox.alert("Ocurrió un error inesperado");
        }
    });
}

/**
 * Función para abrir el formulario de opciones
 * @param id Recibe el id de la pregunta
**/
function agregar_opcion(id) {
    bootbox.dialog({
        message: $('#formulario').html(),
        title: "Opciones",
        buttons: {
            success: {
                label: "Guardar",
                className: "btn-primary",
                callback: function() {
                    submitOption(this);
                }
            },
            close: {
                label: "Cerrar",
                className: "btn-red",
                callback: function() {}
            }
        }
    });
    $('#formulario_modal').append($('#agregar_opciones_base').html());
    $('#formulario_modal').attr('action',id);
}

/**
 * Función para enviar el formulario de las opciones
**/
function submitOption(objecto) {
    var form = $(objecto).find('form');
    $.ajax({
        data: $(form).serialize(), 
        type: 'POST',
        url: '/administrador/consulta/create-option/'+$(form).attr('action'),
        success: function(response) {
            if (response.code) {
                bootbox.alert("Se crearon las opciones con éxito");
            }
            else{
                var errors = '';
                $.each(response.errors,function(key,value){
                    errors += key+" "+value+"<br>";
                });
                bootbox.alert(errors);
            }
        }
    });
}

/**
 * Función para ver las opciones de un pregunta
 * @param id Recibe el id de la pregunta
**/
function see_option(id) {
    $.ajax({
    type: 'GET',
    url: "/administrador/consulta/ajax/opciones-list/"+id,
    success: function(response) {
        if (response.success) {
            var opciones = response.opciones;
            var token = $('input').val();
            var html = '<form action="" role="form" method="post" id="option_form">';
            html += '<input type="hidden" name="csrfmiddlewaretoken" value="'+token+'">';
            $.each(opciones,function(key,value){
                html += "<h4>Opcion #"+parseInt(key+1)+"</h4>";
                html+= $('#agregar_opciones').html();
                html += "<hr>";
            });
            html+= '</form>';
            bootbox.dialog({
                message: html,
                title: "Opciones",
                buttons: {
                    success: {
                        label: "Guardar",
                        className: "btn-primary",
                        callback: function() {
                            update_option(id);
                        }
                    },
                    close: {
                        label: "Cerrar",
                        className: "btn-red",
                        callback: function() {}
                    }
                }
            });
            $.each($('.bootbox-body #option_form #id_texto_opcion'),function(key,value){
                $(value).val(opciones[key]['texto_opcion']);
                $(value).append('<input type="hidden" name="texto_opcion_id" value="'+opciones[key]['id']+'">');
            });
            $.each($('.bootbox-body #option_form #opciones a'),function(key,value){
                $(value).attr('onclick','del_option(this,'+opciones[key]['id']+')');
            });
            }
        },
        error:function(error)
        {
            bootbox.alert("Ocurrió un error inesperado");
        }
    });
}

/**
 * Función para actualizar las opciones de un pregunta
 * @param id Recibe el id de la pregunta
**/
function update_option(id) {
    var form = $("#option_form");
    $.ajax({
        data: $(form).serialize(), 
        type: 'POST',
        url: '/administrador/consulta/update-option',
        success: function(response) {
            if (response.code) {
                bootbox.alert("Se actualizaron las opciones con éxito");
            }
            else{
                var errors = '';
                $.each(response.errors,function(key,value){
                    errors += key+" "+value+"<br>";
                });
                bootbox.alert(errors);
            }
        }
    }); 
}

/**
 * Función para eliminar las opciones de un pregunta
 * @param id Recibe el id de la pregunta
**/
function del_option(element,id) {
        bootbox.dialog({
        message: "¿Desea borrar la opción seleccionada?",
        title: "Alerta",
        buttons: {
            success: {
                label: "Si",
                className: "btn-primary",
                callback: function() {
                    var token = $('input').val();
                    $.ajax({
                        data: {'csrfmiddlewaretoken':token},
                        type: 'POST',
                        url: '/administrador/consulta/delete-option/'+id,
                        success: function(response) {
                            if (response.success) {
                                remove_option(element);
                                bootbox.alert("Se eliminó la opción con éxito");
                            }
                            else {
                                bootbox.alert(response.mensaje);
                            }
                        },
                        error:function(error)
                        {
                            bootbox.alert("Ocurrió un error inesperado");
                        }
                    }); 
                }
            },
            close: {
                label: "No",
                className: "btn-red",
                callback: function() {}
            }
        }
    });
}

/**
 * Función para eliminar una pregunta
 * @param id Recibe el id de la pregunta
**/
function del_pregunta(element,id) {
        bootbox.dialog({
        message: "¿Desea borrar la pregunta seleccionada?",
        title: "Alerta",
        buttons: {
            success: {
                label: "Si",
                className: "btn-primary",
                callback: function() {
                    var token = $('input').val();
                    $.ajax({
                        data: {'csrfmiddlewaretoken':token},
                        type: 'POST',
                        url: '/administrador/consulta/delete-question/'+id,
                        success: function(response) {
                            if (response.success) {
                                remove_option(element);
                                bootbox.alert("Se eliminó la pregunta con éxito");
                            }
                            else {
                                bootbox.alert(response.mensaje);
                            }
                        },
                        error:function(error)
                        {
                            bootbox.alert("Ocurrió un error inesperado");
                        }
                    }); 
                }
            },
            close: {
                label: "No",
                className: "btn-red",
                callback: function() {}
            }
        }
    });
}

/**
 * Función para abrir el formulario de preguntas
 * @param id Recibe el id de la consulta
**/
function add_preguntas(id) {
    var token = $('input').val();
    var html = '<form action="" role="form" method="post" id="question_form">';
    html += '<input type="hidden" name="csrfmiddlewaretoken" value="'+token+'">';
    html += '<div class="content"><h5 class="text-success">Agregar Preguntas '
    html += '<a href="#" onclick="agregar_preguntas(\'#preguntas_base\');">';
    html += '<span class="glyphicon glyphicon-plus text-success"></span></a></h5></div>';
    html += '<div id="agregar_preguntas">';
    html += $('#preguntas_base').html();
    html += '</div></form>';
    bootbox.dialog({
        message: html,
        title: "Preguntas",
        buttons: {
            success: {
                label: "Guardar",
                className: "btn-primary submit-question",
                callback: function() {
                    var vacio = false;
                    $.each($('.modal-body #id_texto_pregunta'),function(key,value){
                        if ($(value).val().trim()=='') {
                            vacio = true;
                        }
                    });
                    $.each($('.modal-body #id_tipo_pregunta'),function(key,value){
                        if ($(value).val().trim()=='') {
                            vacio = true;
                        }
                    });
                    if (vacio) {
                        event.preventDefault();
                        bootbox.dialog({
                            message: "Debe llenar todas las preguntas que agregó",
                            title: "<b class='text-danger'>Error</b>",
                            buttons: {
                                success: {
                                    label: "Cerrar",
                                    className: "btn-red",
                                    callback: function() {}
                                }
                            }
                        });
                    }
                    else{
                        create_question(id);
                    }
                }
            },
            close: {
                label: "Cerrar",
                className: "btn-red",
                callback: function() {}
            }
        }
    });
}

/**
 * Función para crear un pregunta
 * @param id Recibe el id de la consulta
**/
function create_question(id) {
    var form = $("#question_form");
    $.ajax({
    type: 'POST',
    data: $(form).serialize(),
    url: "/administrador/consulta/create-question/"+id,
    success: function(response) {
        if (response.code) {
            bootbox.alert("Se crearon/creó la(s) pregunta(s) con éxito");
        }
        else{
            var errors = '';
            $.each(response.errors,function(key,value){
                errors += key+" "+value+"<br>";
            });
            bootbox.alert(errors);
        }
    },
        error:function(error)
        {
            bootbox.alert("Ocurrió un error inesperado");
        }
    });
}

/**
 * Función para actualizar las preguntas de una consulta
**/
function update_question() {
    var form = $("#question_form");
    $.ajax({
        data: $(form).serialize(), 
        type: 'POST',
        url: '/administrador/consulta/update-question',
        success: function(response) {
            if (response.code) {
                bootbox.alert("Se actualizaron las preguntas con éxito");
            }
            else{
                var errors = '';
                $.each(response.errors,function(key,value){
                    errors += key+" "+value+"<br>";
                });
                bootbox.alert(errors);
            }
        },
        error:function(error)
        {
            bootbox.alert("Ocurrió un error inesperado");
        }
    }); 
}

/**
 * Función para enviar los respuestas de la encuesta
 * @param event Recibe el evento
**/
function send_poll(event) {
    event.preventDefault();
    $('.btn-primary').attr('disabled',true);
    var form = $("#encuesta_form");
    var routes = $(location).attr('pathname').split('/');
    if (routes.length==4) {
        var pk = routes[routes.length-2];
        var obj = routes[routes.length-1];
    }
    else{
        var pk = routes[routes.length-1];
        var obj = pk;
    }
    var participacion;
    $.get('/participacion/ajax/validar-participacion?consulta='+pk+'&objetivo='+obj)
    .done(function(response){
        if (response.mensaje) {
            participacion = response.participacion
            if (participacion) {
                bootbox.alert("Ya participó para esta consulta <br>Será direccionado en 4 segundos");
                setTimeout(function(){
                    $(location).attr('href', $(location).attr('origin')+'/participacion')    
                },4000);
            }
            else
            {
                $.ajax({
                    type: 'POST',
                    data: $(form).serialize(),
                    url: "/participacion/"+pk+"/"+obj,
                    success: function(response) {
                        if (response.code == true) {
                            bootbox.alert("Se registró su participación con éxito <br>Será direccionado en 4 segundos");
                            setTimeout(function(){
                                $(location).attr('href', $(location).attr('origin')+'/participacion')    
                            },4000);
                        }
                        else{
                            bootbox.alert("Ocurrió un error inesperado");
                            $('.btn-primary').attr('disabled',false);
                        }
                    },
                        error:function(error)
                        {
                            bootbox.alert("Ocurrió un error inesperado");
                            $('.btn-primary').attr('disabled',false);
                        }
                });
            }
        }
        else{
            bootbox.alert(response.error);    
        }
        })
    .fail(function(response){
        bootbox.alert("Ocurrió un error inesperado");
    });
}

/**
 * Función para retroceder en el carrusel y bajar el valor de la
 * barra de progreso
**/
function go_back() {
    var first_element = $('.carousel-indicators li')[0];
    if($(first_element).attr('class')!=='active')
    {
        $('#myCarousel').carousel('prev');
        var elements = $('.carousel-indicators li').length-1;
        var current_value = ($('#status .progress-bar').width()/$('#status').width())*100;
        var final_value = current_value-(100/elements);
        $('#status .progress-bar').width(final_value+"%");
        if (final_value!=100) {
            $('#status .bar span').text() == "Finalizado" ? $('#status .bar span').text('Progreso'):'';
            $('#status .progress-bar').removeClass('progress-bar-success');
        }
        if (final_value<=0) {
            $('#status .bar span').css({'color':'black'});
        }
    }
}

/**
 * Función para aumentar la barra de progreso si se responde la encuesta
**/
function control_progress() {
    var content = $('.carousel-inner .active');
    var not_empty = 0;
    var elements = $('.carousel-indicators li').length-1;
    $.each(content.find('input'),function(index,value){
        var name = $(value).attr('name');
        if(name.search('radio')!=-1 || name.search('check')!=-1 || name.search('sino')!=-1){
            not_empty = $(value).parent().attr('class').search('checked') !== -1 ? 1:not_empty;
            if (name.search('sino')!=-1) {
                if ($(value).parent().attr('class').search('checked') !== -1 && $(value).val()=="Si") {
                    if ($(value).attr('class').search('need_justification')!=-1) {
                        var text_area = $(value).parent().parent().find('textarea');
                        not_empty = $(text_area).val().trim() !== '' ? 1:0;
                        not_empty = $(text_area).val().length >= 10 && $(text_area).val().length <= 50  ? 1:0;
                        if ($(text_area).val().length < 10 || $(text_area).val().length >50) {
                            bootbox.alert("La longitud de la respuesta debe estar entre 10 y 50 cáracteres");
                        }
                    } 
                }               
            }
        }
    });
    $.each(content.find('textarea'),function(index,value){
        var name = $(value).attr('name');
        if (name.search('abierta')!==-1) {
            not_empty = $(value).val().trim() !== '' ? 1:not_empty;
            not_empty = $(value).val().length >= 700 && $(value).val().length <= 5000  ? 1:0;
            if ($(value).val().length < 700 || $(value).val().length >5000) {
                bootbox.alert("La longitud de la respuesta debe estar entre 700 y 5000 cáracteres");
            }
        }
    });
    if (not_empty) {
        $('#status .bar span').css({'color':'white'});
        $('#myCarousel').carousel('next');
        var current_value = ($('#status .progress-bar').width()/$('#status').width())*100;
        var final_value = current_value+(100/elements);
        $('#status .progress-bar').width(final_value+"%");
        
        if (final_value>=99.9) {
            $('#status .progress-bar').width("100%");
            $('#status .bar span').text("Finalizado");
            $('#status .progress-bar').addClass('progress-bar-success');
        }
    }
}


/**
 * Función que crea los textos
 */
function create_text_files(pk){
    $.ajax({
        type: 'GET',
        url: "/administrador/consulta/ajax/generar-textos-respuesta/"+pk,
        success: function(response) {
            bootbox.alert(response.mensaje);
        },
        error:function(error){
                bootbox.alert("Ocurrió un error inesperado");
        }
    });
}


/**
 * @brief Función que actualiza los datos de combos dependientes
 * @param opcion Código del elemento seleccionado por el cual se filtrarán los datos en el combo dependiente
 * @param app Nombre de la aplicación en la cual buscar la información a filtrar
 * @param mod Modelo del cual se van a extraer los datos filtrados según la selección
 * @param campo Nombre del campo con el cual realizar el filtro de los datos
 * @param n_value Nombre del campo que contendra el valor de cada opción en el combo
 * @param n_text Nombre del campo que contendrá el texto en cada opción del combo
 * @param combo_destino Identificador del combo en el cual se van a mostrar los datos filtrados
 * @param bd Nombre de la base de datos, si no se específica se asigna el valor por defecto
 */
function actualizar_combo(opcion, app, mod, campo, n_value, n_text, combo_destino, bd) {
    /* Verifica si el parámetro esta definido, en caso contrario establece el valor por defecto */
    bd = typeof bd !== 'undefined' ? bd : 'default';
    $.ajaxSetup({
        async: false
    });
    $.getJSON('/ajax/actualizar-combo/', {
        opcion:opcion, app:app, mod:mod, campo:campo, n_value:n_value, n_text: n_text, bd:bd
    }, function(datos) {

        var combo = $("#"+combo_destino);

        if (datos.resultado) {

            if (datos.combo_disabled == "false") {
                combo.removeAttr("disabled");
            }
            else {
                combo.attr("disabled", "true");
            }

            combo.html(datos.combo_html);
        }
        else {
            bootbox.alert(datos.error);
            console.log(datos.error);
        }
    }).fail(function(jqxhr, textStatus, error) {
        var err = textStatus + ", " + error;
        bootbox.alert( 'Petición fállida' + err );
        console.log('Petición fállida ' + err)
    });
}

/**
 * @brief Función para recargar el captcha vía json
 * @param element Recibe el botón
 */
function refresh_captcha(element) {
    $form = $(element).parents('form');
    var url = location.protocol + "//" + window.location.hostname + ":" + location.port + "/captcha/refresh/";

    $.getJSON(url, {}, function(json) {
        $form.find('input[name="captcha_0"]').val(json.key);
        $form.find('img.captcha').attr('src', json.image_url);
    });

    return false;
}

/**
 * @brief Función para mostrar un campo
 * @param valor Recibe el valor
 * @param condicion Recibe la condición a evaluar
 * @param element Recibe el elemento a habilitar
 */
function mostrar(valor,condicion,element) {
    if (valor==condicion) {
        $('#'+element).show();
    }
    else{
        $('#'+element).hide();
    }
}

/**
 * @brief Función para habilitar/deshabilitar un campo
 * @param valor Recibe el valor
 * @param condicion Recibe la condición a evaluar
 * @param element Recibe el elemento a modificar
 * @param attr_name Recibe el nombre del atributo a agregar/remover
 */
function habilitar(valor,condicion,element,attr_name) {
    if (valor!=condicion) {
        $('#'+element).attr(attr_name,true)
    }
    else{
        $('#'+element).removeAttr(attr_name);
    }
}

/**
 * @brief Función para mostrar los sectores
 * @param valor Recibe el valor
 */
function mostrar_sector(valor) {
    mostrar(valor,'ES','sector_estudiante');
    mostrar(valor,'TR','sector_trabajador'); 
}

/**
 * @brief Función para validar si pertenece a un colectivo
 * @param valor Recibe el valor
 */
function habilitar_colectivo(valor) {
    habilitar(valor,'CO','id_colectivo','readonly');
}

function medir_caracters(obj) {
    var span = $(obj).parent().find('#longitud span');
    span.text($(obj).val().length);
}
