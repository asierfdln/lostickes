Widget rápido de prueba en la página principal para hacer cuentas rápidas sin
necesidad de logearse...

--------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------
---------------------------------------------- TO-DO ----------------------------------------------
--------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------


--------------------------------------------------------------------------------------------------
--------------------------------------------- iraxe ----------------------------------------------
--------------------------------------------------------------------------------------------------

@iraxe mensajitos en inputs de createDebt

@iraxe deberiamos poder ver / no ver las transacciones pagadas
    QUE SE OCULTEN CON VUEeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
    habria que implementarlo en "debts" y en "group"

@iraxe comentar un poco el codigo de vue para la posteridad porsiaca

@iraxe checkboxes de delete transactions (que sea tipo mark_aspayed() y que desaparezcan?)

    (1) que el boton primero tenga el texto de "seleccionar transactions"
    (2) click
    (3) cambiar el texto del boton a delete transactions
    (4) que salgan los checkboxes
    (5) (seleccionas por lo menos uno para poder hacer lo de eliminar)
    (6) que el boton tenga una view.func con solo codigo de eliminar de
        base de datos las transacciones y te redirija a group/

    (7*) idealmente, que solo el owner de las transacciones pueda borrar las transacciones...

@iraxe colores en funcion de PAYED - OWNER - OWS...

@iraxe que la columna del medio en las vistas de "debt" se ajuste al texto (se ve mal lo de PAYED, OWS, OWNER)...


--------------------------------------------------------------------------------------------------
--------------------------------------------- asier ----------------------------------------------
--------------------------------------------------------------------------------------------------

redirect('login', argumentos...)
mirar esto de fieldset para las forms a ver si ambia algo... (mirar register.html)
lo mismo con lo del outline de los botones

-> comentar los formatos de contexts...
-> mover js's a static...
-> logins y usuarios (mirar video de logins de coreyschafer)
-> message forms (mirar video de logins de coreyschafer)
-> piechart con info de balances justo debajo del cosobox este que flota de irache (d3.js????????)

-> i18n
--> help texts fuera...

-> html <select> para usuarios...

-> modify debt, de clickar en una propia transaccion desde la vista de deuda y que te lleve a 
   una vista de eliminacion de campos

-> checkear que no te han jodido con mangling de datos con get_object_or_404()

-> try-except en form.isvalid() para salir en cuanto "todo_bien = False"

    con clases de Exception tipo
    class ExceptionPayerNoEnTransaccion(Exception):
        pass