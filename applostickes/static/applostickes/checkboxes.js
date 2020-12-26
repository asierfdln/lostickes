$(document).ready(function () {

    // codigo para habilitar/deshabilitar checkboxes con cada elemento.checkbox
    $('input[id^=id_elements_').each(function () {

        // numero de elemento
        var numero_de_check = $(this).prop('id').slice(-1);

        // cuando hacemos click en el elemento de comida
        $(this).click(function () {

            // si esta el bisho checkeado, me habilitas todas las weas de debajo (All, pepe, juan...)
            if ($(this).is(":checked")) {
                // habilitamos el All
                $('input[id="checkall_id_elements_' + numero_de_check + '"]').each(function () {
                    $(this).prop("disabled", false);
                });
                // habilitamos a pepe, juan...
                $('input[name="people_paying_element_' + numero_de_check + '"]').each(function () {
                    $(this).prop("disabled", false);
                });

            // si no esta el bisho checkeado, me deshabilitas todas las weas de debajo (All, pepe, juan...)
            } else {
                // deshabilitamos el All
                $('input[id="checkall_id_elements_' + numero_de_check + '"]').each(function () {
                    $(this).prop("disabled", true);
                });
                // deshabilitamos a pepe, juan...
                $('input[name="people_paying_element_' + numero_de_check + '"]').each(function () {
                    $(this).prop("disabled", true);
                });
            }
        });

        // codigo de checkbox All
        $('input[id="checkall_id_elements_' + numero_de_check + '"').click(function () {

            // si el All esta checkiado, me checkeas a pepe, juan...
            if ($(this).is(":checked")) {
                $('input[name="people_paying_element_' + numero_de_check + '"]').each(function () {
                    $(this).prop("checked", true);
                });

            // si el All no esta checkiado, me descheckeas a pepe, juan...
            } else {
                $('input[name="people_paying_element_' + numero_de_check + '"]').each(function () {
                    $(this).prop("checked", false);
                });
            }
        });

        // codigo de cada checkbox independiente cuando le das a All
        $('input[name="people_paying_element_' + numero_de_check + '"]').bind('change', function () {
            if ($('input[name="people_paying_element_' + numero_de_check + '"]').filter(':not(:checked)').length == 0) {
                $('#checkall_id_elements_' + numero_de_check + '').prop("checked", true);
            } else {
                $('#checkall_id_elements_' + numero_de_check + '').prop("checked", false);
            }
        });

        // cuando volvemos de una form no valida... (un poco ñapa)
        // si esta el bisho checkeado, me habilitas todas las weas de debajo (All, pepe, juan...)
        if ($(this).is(":checked")) {
            $('#checkall_id_elements_' + numero_de_check + '').click()
        } else {
            // comenzamos con checkboxes deshabilitados
            $('input[id="checkall_id_elements_' + numero_de_check + '"]').each(function () {
                $(this).prop("disabled", true);
            });
            $('input[name="people_paying_element_' + numero_de_check + '"]').each(function () {
                $(this).prop("disabled", true);
            });
        }
    });
});