COSAS PENDIENTES PARA LA SIGUIENTE ENTREGA

 - Pulir el modelo de datos y añadir roles y clases intermedias (inlines) 
   para tener un modelo más completo.

 - Uso de signals m2m (many to many) para la actualización de valores
   y cuentas de cada usuario.

 - Mejora de formulario de creacion de deuda con AJAX, o cargar el propio set
   de usuarios disponibles en función del grupo donde estés definiendo la
   deuda. Asignación de deudas y cuentas con los roles y clases intermedias.

 - Fecha de creacion de elementos para su ordenación. Diferentes opciones de
   orden de elementos (alfabetico, asc desc, ultimo creado...).

 - Mejora de la interfaz gráfica de los formularios.

 - Implementacion de sistema de usuarios (bien hecho, no como ahora visto todo 
   desde "USER" en views...). Subsecuente implementación de funcionalidad al
   botón de pagar. Botón de "Marcar como pagado" para el propietario de la deuda.

 - Widget rápido de prueba en la página principal para hacer cuentas rápidas sin
   necesidad de logearse.


-- TODO --

@iraxe mensajitos en inputs de createDebt

@iraxe comentar un poco el codigo de vue para la posteridad porsiaca

@iraxe checkboxes de delete transactions: (TODO @asier pensar db si peta o no...)

    (1) que el boton primero tenga el texto de "seleccionar transactions"
    (2) click
    (3) cambiar el texto del boton a delete transactions
    (4) que salgan los checkboxes
    (5) (seleccionas por lo menos uno para poder hacer lo de eliminar)
    (6) que el boton tenga una view.func con solo codigo de eliminar de
        base de datos las transacciones y te redirija a group/

    (7*) idealmente, que solo el owner de las transacciones pueda borrar las transacciones...


-> MIRAR TODOS LOS BALANCES Y QUE DEPENDAN DEL SCORE_SETTLING...
-> mover js's a static...
-> desc en elements sobra
-> quitar lo de OWNER en views...
-> PAGAR
--> necesario un diccionario de score-settling en el que lleves cuenta de
    {'primkey_user': [role, pagado/no]}, y en funcion del estado de ese dicc pues 
    renderizas la cuenta o no
--> boton de "Debt settled" con correspondiente funcionalidad de borrar
-> logins y usuarios (mirar video de logins de coreyschafer)
-> message forms (mirar video de logins de coreyschafer)
-> piechart con info de balances justo debajo del cosobox este que flota de irache (d3.js????????)
-> i18n
--> help texts fuera...
-> modify debt, de clickar en una propia transaccion desde la vista de deuda y que te lleve a 
   una vista de eliminacion de campos
-> try-except en form.isvalid() para salir en cuanto "todo_bien = False"

    con clases de Exception tipo
    class ExceptionPayerNoEnTransaccion(Exception):
        pass