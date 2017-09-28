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
function send_poll() {
    $('.submit').attr('disabled',true);
    var form = $("#encuesta_form");
    var routes = $(location).attr('pathname').split('/');
    var pk = routes[routes.length-1];
    var participacion;
    $.get(URL_VALIDAR_PARTICIPACION+'?consulta='+pk)
    .done(function(response){
        if (response.mensaje) {
            participacion = response.participacion
            if (participacion) {
                MaterialDialog.alert("Ya participó en esta consulta <br>Será direccionado en 4 segundos",{
                    'title':"Error",
                    'buttons':{'close':{'text':'cerrar'}}
                });
                setTimeout(function(){
                    $(location).attr('href', URL_PARTICIPACION)    
                },4000);
            }
            else
            {
                $.ajax({
                    type: 'POST',
                    data: $(form).serialize(),
                    url: URL_REGISTRAR_PARTICIPACION+pk,
                    success: function(response) {
                        if (response.code == true) {
                            MaterialDialog.alert("Se registró su participación con éxito <br>Será direccionado en 4 segundos",{
                                'title':"Éxito",
                                'buttons':{'close':{'text':'cerrar'}}
                            });
                            setTimeout(function(){
                                $(location).attr('href', URL_PARTICIPACION)    
                            },4000);
                        }
                        else{
                            MaterialDialog.alert("Ocurrió un error inesperado",{
                                'title':"Error",
                                'buttons':{'close':{'text':'cerrar'}}
                            });
                            $('.btn').attr('disabled',false);
                        }
                    },
                        error:function(error)
                        {
                            MaterialDialog.alert("Ocurrió un error inesperado",{
                                'title':"Error",
                                'buttons':{'close':{'text':'cerrar'}}
                            });
                            $('.btn').attr('disabled',false);
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
 * Función para aumentar la barra de progreso si se responde la encuesta
**/
function control_progress() {
    var content = $('.swiper-slide-active');
    var not_empty = 0;
    $.each(content.find('input'),function(index,value){
        var name = $(value).attr('name');
        if(name.search('radio')!=-1 || name.search('check')!=-1 || name.search('sino')!=-1){
            not_empty = $(value).is(":checked") ? 1:not_empty;
            if (name.search('sino')!=-1) {
                if ($(value).is(":checked") && $(value).val()=="Si") {
                    if ($(value).attr('class')) {
                        if ($(value).attr('class').search('need_justification')!=-1) {
                            var text_area = $(value).parent().parent().find('textarea');
                            not_empty = $(text_area).val().trim() !== '' ? 1:0;
                            not_empty = $(text_area).val().length >= 10 && $(text_area).val().length <= 50  ? 1:0;
                            if ($(text_area).val().length < 10 || $(text_area).val().length >50) {
                                MaterialDialog.alert("La longitud de la respuesta debe estar entre 10 y 50 cáracteres",{
                                    'title':"Alerta",
                                    'buttons':{'close':{'text':'cerrar'}}
                                });
                            }
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
            not_empty = $(value).val().trim().length >= 10 && $(value).val().trim().length <= 50  ? 1:0;
            if ($(value).val().length < 10 || $(value).val().length >50) {
                MaterialDialog.alert("La longitud de la respuesta debe estar entre 10 y 50 cáracteres",{
                    'title':"Alerta",
                    'buttons':{'close':{'text':'cerrar'}}
                });
            }
        }
    })
    return not_empty;
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
 * @brief Función para medir la cantidad de caracteres escritos
 * en el input
 * @param obj Recibe el input en la función oninput
 */
function medir_caracters(obj) {
    var span = $(obj).parent().find('#longitud span');
    span.text($(obj).val().trim().length);
}

/**
 * @brief Función para quitar doble espacios en el input
 * @param obj Recibe el input en la función oninput
 */
function quitar_espacios(obj) {
    $(obj).val($(obj).val().replace("  ",""));
}
