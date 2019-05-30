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
        MaterialDialog.alert("Ocurrió un error inesperado",{
            'title':"Error",
            'buttons':{'close':{'text':'cerrar'}}
        });
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

/**
 * @brief Función buscar los datos del municipio
 * @param valor Recibe el valor del select
 */
function get_municipio(valor) {
    if (valor!='') {
        var url = URL_BUSCAR_MUNICIPIO+'?entidad='+valor;
    }
    else{
        var url = URL_BUSCAR_MUNICIPIO;
        $('#id_municipio').attr('disabled',true);
        $('#id_municipio').formSelect();
    }
    $.get(url)
        .done(function(response){
            $('#id_municipio').removeAttr('disabled');
            var html = json2html_select(response);
            $('#id_municipio').html(html);
            $('#id_municipio').formSelect();
        })
        .fail(function(response){
            MaterialDialog.alert("Ocurrió un error inesperado",{
                'title':"Error",
                'buttons':{'close':{'text':'cerrar'}}
            });
        });
}

/**
 * @brief Función buscar los datos de la parroquia
 * @param valor Recibe el valor del select
 */
function get_parroquia(valor) {
    if (valor!='') {
        var url = URL_BUSCAR_PARROQUIA+'?municipio='+valor;
    }
    else{
        var url = URL_BUSCAR_PARROQUIA;
        $('#id_parroquia').attr('disabled',true);
        $('#id_parroquia').formSelect();
    }
    $.get(url)
        .done(function(response){
            $('#id_parroquia').removeAttr('disabled');
            var html = json2html_select(response);
            $('#id_parroquia').html(html);
            $('#id_parroquia').formSelect();
        })
        .fail(function(response){
            MaterialDialog.alert("Ocurrió un error inesperado",{
                'title':"Error",
                'buttons':{'close':{'text':'cerrar'}}
            });
        });
}

/**
 * @brief Función para convertir el json del select en el html correspondiente
 * @param data Recibe los valores en formato JSON
 * @return html Retorna los datos transformados en HTML
 */
function json2html_select(data) {
    var html = '';
    $.each(data,function(key,value){
        html += '<option value="'+value[0]+'">'+value[1]+'</option>';
    });
    return html;
}

/**
 * @brief Función para mostrar la justificación de las
 * respuestas de Si/No
 * @param element Recibe el elemento
 * @param show Recibe si se motrará o se ocultará
 */
function show_justification(element,show) {
    var id = $(element).attr("name").split("_");
    id = id[id.length-1];
    if (show) {
        $('#div_justificar_'+id).show();
    }
    else{
        $('#div_justificar_'+id).hide();
    }
}