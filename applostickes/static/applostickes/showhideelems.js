$(document).ready(function () {
    $('#btnShHd').click(function () {
        if ($(this).prop('innerText') == 'Hide old elements') {
            $(this).prop('innerText', 'Show old elements');
            // hide stuff
            // $('#ultohide').prev().prev().hide();
            // $('#ultohide').prev().hide();
            $('#ultohide').hide();
        } else {
            $(this).prop('innerText', 'Hide old elements');
            // show stuff
            // $('#ultohide').prev().prev().show();
            // $('#ultohide').prev().show();
            $('#ultohide').show();
        }
    });
});