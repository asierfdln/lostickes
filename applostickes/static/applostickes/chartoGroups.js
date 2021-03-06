$(document).ready(function () {

    function getData() {
        $('h4[id=nombre_grupo]').each(function () {
            jq_labels.push($(this).prop('innerText'));
        });
        $('p[id=balance_grupo]').each(function () {
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

    jq_data.forEach(element => {
        if (element == 0.0) {
            colourz.push('rgb(0, 0, 0)'); // no se va a ver, da igual el color...
        } else if (element > 0) {
            colourz.push('rgb(255, 99, 132)'); // rojo
        } else {
            colourz.push('rgb(99, 255, 132)'); // verde
        }
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
            tooltips: {
                enabled: true
            }
        }
    });
});