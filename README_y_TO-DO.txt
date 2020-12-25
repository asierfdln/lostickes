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

i18n
colorcico de la navbar el mismo que el del boton de signup

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