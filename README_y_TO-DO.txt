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

 - Cambio de color de elementos de deuda/grupo en función de balance.

 - Implementacion de sistema de usuarios (bien hecho, no como ahora visto todo 
   desde "USER" en views...). Subsecuente implementación de funcionalidad al
   botón de pagar. Botón de "Marcar como pagado" para el propietario de la deuda.

 - Widget rápido de prueba en la página principal para hacer cuentas rápidas sin
   necesidad de logearse.


-- TODO --

@iraxe los popup forms https://pypi.org/project/django-popup-forms/

eurosdubidu en COste DESPUES DE QUE IRAXE HAGA LAS TEMPLATES METES LOS EUROS 
DONDEQUIERAS MIJO

-> PAGAR (signals o refresh?? boton con funcionalidad??.............)

-> checkboxes
--> asegurarse de que los checkboxes de los users estan clickados (por lo menos 
    uno...) cuando le damos a Submit si (1) el checkbox superior de elemento 
    está clickado.

-> message forms (mirar video de logins de coreyschafer)

-> logins y usuarios (mirar video de logins de coreyschafer)

-> EXTRAS
--> piechart con info de balances justo debajo del cosobox este que flota de 
    irache
--> poner los divs clickables limitados cambiando div por <a>