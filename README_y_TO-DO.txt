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

@iraxe los popup forms https://pypi.org/project/django-popup-forms/
@iraxe cuando entras en http://localhost:8000/group/group1-56f3cf4b el "Balance" tb en colores
@iraxe mirar video de clase de web de hoy y meter con vue la verga esta de elementos nuevos...

-> createDEBt hacer bien lo de pagadores de la transaccion, no por cada leche
-> AAAAAAAAAAAAAAAAA comprobacion server de checkboxes AAAAAAAAAAAAAAAAA
-> modify debt, de clickar en una propia transaccion desde la vista de deuda y que te lleve a 
   una vista de eliminacion de campos
-> PAGAR
--> boton que tenga codigo dentro y te redireccione a la pag web en la que estabas
--> que aparezca el boton si eres deudor, no pagador
---> que aparezca un boton de borrar deuda si eres pagador
--> necesario un diccionario de score-settling en el que lleves cuenta de
    {'primkey': [role, pagado/no]}, y en funcion del estado de ese dicc pues 
    renderizas la cuenta o no
-> logins y usuarios (mirar video de logins de coreyschafer)
-> message forms (mirar video de logins de coreyschafer)

-> EXTRAS
--> piechart con info de balances justo debajo del cosobox este que flota de 
    irache