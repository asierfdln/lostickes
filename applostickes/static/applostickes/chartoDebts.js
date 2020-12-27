$(document).ready(function () {

    function getData() {
        $('h4[id=nombre_transaccion]').each(function () {
            jq_labels.push($(this).prop('innerText'));
        });
        $('p[name=bal]').each(function () {
            var texto = $(this).prop('innerText');
            var numero = texto.replace(/[^0-9\.]+/g, '');
            if (texto.includes('-')) {
                jq_data.push(numero * -1);
            } else {
                jq_data.push(numero);
            }
        });
    }

    // cogemos la tarta
    var ctx = document.getElementById('myChart').getContext('2d');

    // definicion de variables
    var jq_labels = [];
    var jq_data = [];
    var colourz = [];

    // carga de variables
    getData();

    var precio_total_usuario = 0; // suma total de lo que pagas
    jq_data.forEach(element => {
        if (element == 0.0) {
            colourz.push('rgb(0, 0, 0)'); // no se va a ver, da igual el color...
        } else if (element > 0) {
            colourz.push('rgb(255, 99, 132)'); // rojo
        } else {
            colourz.push('rgb(99, 255, 132)'); // verde
        }
        console.log('element');
        console.log(element);
        console.log('precio_total_usuario');
        console.log(precio_total_usuario);
        precio_total_usuario = (Number(precio_total_usuario) + Number(element)).toFixed(2);
        console.log('precio_total_usuarioooooooooooooooooo');
        console.log(precio_total_usuario);
    });

    // pintamos la tarta
    var chart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: jq_labels,
            datasets: [{
                backgroundColor: colourz,
                borderColor: 'rgb(255, 255, 255)',
                data: jq_data
            }]
        },
        options: {
            legend: {
                display: false
            },
            title: {
                display: true,
                text: 'Total: ' + precio_total_usuario + ' lereles'
            },
            tooltips: {
                enabled: true
            }
        }
    });
});