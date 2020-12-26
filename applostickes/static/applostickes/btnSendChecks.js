$(document).ready(function () {

    $('#btnSend').click(function (e) {

        // variable apra controlar/mirar si hay mas de un mensaje de error o no
        var primer_if_trig = 0;

        // miramos que no se nos ha pasado ningun elemento de comida vacio y que se ha añadido alguno

        // variable para controlar el checkeo de elementos
        // var flag_algun_comido_checkeado = 0; // TODO @asier
        var flag_algun_person_checkeado = 0;

        // cogemos todos los elementos de comida e iteramos sobre ellos
        $('input[id^=id_elements_').each(function () {
            var numero_de_comida = $(this).prop('id').replace(/[^0-9\.]+/g, "");
            // si el elemento comida esta checkeado...
            if ($(this).is(":checked")) {

                // flag_algun_comido_checkeado = 1; // TODO @asier

                // iteramos por cada una de las personas del elemento comida...
                $('input[name^=people_paying_element_' + numero_de_comida + ']').each(function () {
                    // si hay alguna persona checkeada, pues lo marcamos...
                    if ($(this).is(":checked")) {
                        flag_algun_person_checkeado = 1;
                    }
                });
                // si no hay ninguna checkeada...
                if (flag_algun_person_checkeado == 0) {
                    // problemas
                    $("#elements-alerts").empty();
                    $("#elements-alerts").prepend(
                        '<div id="div-alert" class="alert alert-danger">' +
                        '<span style="color: red;">' +
                        '<ul class="errorlist">' +
                        '<li>' +
                        'Hay elementos sin usuarios checkeados.' +
                        '</li>' +
                        '</ul>' +
                        '</span>' +
                        '</div>'
                    );
                    primer_if_trig = 1;
                    e.preventDefault();
                }
            }
        });

        // if (flag_algun_comido_checkeado == 0) {
        //     console.log("que no hay naaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa");
        //     if (primer_if_trig > 0) {
        //         $("#div-alert").prepend(
        //             '<span style="color: red;">' +
        //             '<ul class="errorlist">' +
        //             '<li>' +
        //             'No has añadido ningún elemento a la transaccion.' +
        //             '</li>' +
        //             '</ul>' +
        //             '</span>'
        //         );
        //     } else {
        //         $("#elements-alerts").empty();
        //         $("#elements-alerts").prepend(
        //             '<div id="div-alert" class="alert alert-danger">' +
        //             '<span style="color: red;">' +
        //             '<ul class="errorlist">' +
        //             '<li>' +
        //             'No has añadido ningún elemento a la transaccion.' +
        //             '</li>' +
        //             '</ul>' +
        //             '</span>' +
        //             '</div>'
        //         );
        //         primer_if_trig = 1
        //         e.preventDefault();
        //     }
        // } else {
        //     console.log("que siiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii");
        // }

        // miramos que el tema de las personas este bien planteado

        var num_de_users_por_elemento = $("[id^=persona_]").length / $("[id^=id_elements_]").length;
        var array_users_implicados = [];
        $('input[id^=persona_]').each(function () {
            if (!array_users_implicados.includes($(this).val()) && $(this).prop('checked') && !$(this).prop('disabled')) {
                array_users_implicados.push($(this).val())
            }
        });
        var user_pagador = $('select[id="id_payer"]').val();
        if (array_users_implicados.length == 1) {
            if (primer_if_trig > 0) {
                $("#div-alert").prepend(
                    '<span style="color: red;">' +
                    '<ul class="errorlist">' +
                    '<li>' +
                    'No puedes tener un único usuario en la transaccion.' +
                    '</li>' +
                    '</ul>' +
                    '</span>'
                );
            } else {
                $("#elements-alerts").empty();
                $("#elements-alerts").prepend(
                    '<div id="div-alert" class="alert alert-danger">' +
                    '<span style="color: red;">' +
                    '<ul class="errorlist">' +
                    '<li>' +
                    'No puedes tener un único usuario en la transaccion.' +
                    '</li>' +
                    '</ul>' +
                    '</span>' +
                    '</div>'
                );
                primer_if_trig = 1
                e.preventDefault();
            }
        }

        // if (flag_algun_comido_checkeado == 1 && flag_algun_person_checkeado == 1) { // TODO @asier
        if (flag_algun_person_checkeado == 1) {
            if (!array_users_implicados.includes(user_pagador)) {
                if (primer_if_trig > 0) {
                    $("#div-alert").prepend(
                        '<span style="color: red;">' +
                        '<ul class="errorlist">' +
                        '<li>' +
                        'El pagador no tiene nada en la transaccion.' +
                        '</li>' +
                        '</ul>' +
                        '</span>'
                    );
                } else {
                    $("#elements-alerts").empty();
                    $("#elements-alerts").prepend(
                        '<div class="alert alert-danger">' +
                        '<span style="color: red;">' +
                        '<ul class="errorlist">' +
                        '<li>' +
                        'El pagador no tiene nada en la transaccion.' +
                        '</li>' +
                        '</ul>' +
                        '</span>' +
                        '</div>'
                    );
                    e.preventDefault();
                }
            }
        }
    });
});