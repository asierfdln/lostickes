$(document).ready(function () {

    function getData() {
        var nombre_usuario_loggeado = $('#dropdownMenuButton').prop('innerText').slice(1);
        var presio_total = 0;
        var num_de_mens = 0;
        var presio_usuario = 0;
        $('p[id=compra_elemento]').each(function () {
            if ($(this).parent().next().prop('innerText').includes(nombre_usuario_loggeado)) {
                jq_labels.push($(this).prop('innerText'));
                presio_total = $(this).parent().next().next().prop('innerText').replace(/[^0-9\.]+/g, '');
                num_de_mens = $(this).parent().next().prop('innerText').split(',').length;
                presio_usuario = (presio_total / num_de_mens).toFixed(2);
                jq_data.push(presio_usuario);
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

    // var precio_total_usuario = jq_data.reduce((a, b) => a + b, 0); // suma total de lo que pagas
    var precio_total_usuario = 0; // suma total de lo que pagas
    var relacion = Math.floor(255 / jq_data.length);
    var blue_comp = 0;
    jq_data.forEach(element => {
        colourz.push('rgb(23, 162, ' + blue_comp + ')');
        blue_comp = blue_comp + relacion;
        precio_total_usuario = (Number(precio_total_usuario) + Number(element)).toFixed(2);
        // console.log(element);
        console.log(precio_total_usuario);
    });

    console.log(precio_total_usuario);

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