from django import forms
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import UserForm, UserGroupForm, TransactionForm
from .models import User, UserGroup, Transaction, Element
import applostickes


user_to_work_with = None


def about(request):
    return render(request, 'applostickes/about.html', {'title': 'About'})


def main(request):
    return render(request, 'applostickes/main.html', {'title': 'Main'})


def register(request):

    context = {}

    # creamos el formulario
    form = UserForm(request.POST or None)

    # si el formulario lleva una request de tipo POST y la info es valida
    if form.is_valid():
        # creamos el objeto de DjangoUser
        django_user_creadoahora = form.save()
        # creamos un usuario de nuestro modelo de datos
        user_modelonuestro = User(django_user=django_user_creadoahora)
        # lo guardamos en base de datos
        user_modelonuestro.save()
        # cargamos un mensajito para la siguiente pagina
        messages.success(request, "User signed up, let's try it out...")
        # nos vamos a login
        return redirect('login')

    context['form'] = form

    return render(request, 'applostickes/register.html', context)

def logout_view(request):

    global user_to_work_with

    user_to_work_with = None

    # cerramos sesion del usuario
    logout(request)
    #cargamos un mensaje para la siguiente view
    messages.success(request, 'You have been logged out, see ya soon!')
    # redirigimos a main
    return redirect('main')


@login_required
def user(request):

    global user_to_work_with

    if user_to_work_with is None:
        user_to_work_with = User.objects.get(django_user__username=request.user.username)

    context = {}

    # los grupos que vemos en la apagina son todos en los que el usuario esta metido
    groups_to_display = user_to_work_with.usergroup_set.all()
    context['groups'] = {}

    # metemos el balance de grupo del usuario para que se vea
    for group in groups_to_display:
        group_balance = group.user_balance(user_pk=user_to_work_with.primkey)
        context['groups'][group.name] = group_balance

    # cogemos todas las transacciones en las que esta involucrado el usuario
    transactions_to_display = user_to_work_with.transaction_set.all()
    context['transactions'] = {}

    # solo vemos las que debe/le deben pasta
    for transaction in transactions_to_display:
        balance_user_transaction = transaction.user_account(user_pk=user_to_work_with.primkey)
        if balance_user_transaction != 0:
            context['transactions'][transaction.name] = balance_user_transaction

    context['title'] = 'User'
    context['nameClass'] = 'User'
    context['username'] = user_to_work_with.django_user.username

    return render(request, 'applostickes/user.html', context)


@login_required
def groups(request):

    global user_to_work_with

    if user_to_work_with is None:
        user_to_work_with = User.objects.get(django_user__username=request.user.username)

    # marcamos que hemos entrado en la vista de groups para luego utilizar esto en la vista de debt...
    applostickes.debts_or_group_enter_point_to_debt_0_or_1 = 1

    context = {}

    # cogemos todos los grupos en los que esta metido el usuario
    groups_to_display = user_to_work_with.usergroup_set.all()
    context['groups'] = {}

    for group in groups_to_display:

        # metemos infor del grupo
        context['groups'][group.name] = [
            group.desc,
            group.user_balance(user_pk=user_to_work_with.primkey),
            [],
            group.get_ugidentifier(),
        ]

        # sacamos todas las transacciones del grupo en las que esta metido el user
        transactions_of_group_with_user = group.transaction_set.filter(payers__primkey=user_to_work_with.primkey)

        # metemos la info de cada transaccion
        for transaction in transactions_of_group_with_user:
            balance_user_transaction = transaction.user_account(user_pk=user_to_work_with.primkey)
            if balance_user_transaction != 0:
                context['groups'][group.name][2].append(
                    [
                        transaction.name,
                        transaction.user_account(user_pk=user_to_work_with.primkey)
                    ]
                )

    context['title'] = 'Groups'
    context['nameClass'] = 'Groups'
    context['username'] = user_to_work_with.django_user.username

    return render(request, 'applostickes/groups.html', context)


@login_required
def debts(request):

    global user_to_work_with

    if user_to_work_with is None:
        user_to_work_with = User.objects.get(django_user__username=request.user.username)

    # marcamos que hemos entrado en la vista de debts para luego utilizar esto en la vista de debt...
    applostickes.debts_or_group_enter_point_to_debt_0_or_1 = 0

    context = {}

    context['debts'] = {}

    # cogemos todas las transacciones en las que esta metido el usuario
    transactions_of_user = Transaction.objects.filter(payers__primkey__contains=user_to_work_with.get_uidentifier())

    for transaction in transactions_of_user:

        # metemos informacion
        context['debts'][transaction.name] = [
            transaction.desc,
            transaction.user_group.name,
            transaction.total_price(),
            transaction.user_account(user_pk=user_to_work_with.primkey),
            [],
            transaction.get_tridentifier(),
            transaction.user_group.get_ugidentifier(),
        ]

        # cogemos a cada usuario y su rol en la transaccion (estado si es que ha pagado...)
        for payer in transaction.payers.all():
            payer_name = payer.django_user.username
            if transaction.get_score_role(payer.primkey) == 'OWNER':
                payer_name = payer_name + ' (OWNER)'
            elif transaction.get_score_role(payer.primkey) == 'DEBTER':
                if transaction.get_score_state(payer.primkey) == 'PAYED':
                    payer_name = payer_name + ' (PAYED)'
                elif transaction.get_score_state(payer.primkey) == 'NOTPAYED':
                    payer_name = payer_name + ' (OWS)'

            context['debts'][transaction.name][4].append(payer_name)

    context['title'] = 'Debts'
    context['nameClass'] = 'Debts'
    context['username'] = user_to_work_with.django_user.username

    return render(request, 'applostickes/debts.html', context)


@login_required
def createGroup(request):

    global user_to_work_with

    if user_to_work_with is None:
        user_to_work_with = User.objects.get(django_user__username=request.user.username)

    applostickes.user_primkey_exclude = user_to_work_with.primkey

    context = {}

    form = UserGroupForm(request.POST or None)

    if form.is_valid():
        from pprint import pprint
        request_as_dict = dict(request.POST)
        pprint(request_as_dict)
        # form.save()
        # return redirect('groups')

    context['form'] = form
    context['title'] = 'Create group'
    context['nameClass'] = 'Create group'
    context['username'] = user_to_work_with.django_user.username

    return render(request, 'applostickes/createGroup.html', context)


@login_required
def group(request, groupName, group_identifier):

    global user_to_work_with

    if user_to_work_with is None:
        user_to_work_with = User.objects.get(django_user__username=request.user.username)

    # indicamos que venimos desde la vista de group para cuando le demos a pagar deuda...
    applostickes.from_group_view_url_string = f'{groupName}-{group_identifier}'

    context = {}

    # cogemos el grupo de usuarios de identificador "group_identifier"
    group_to_display = UserGroup.objects.get(primkey__contains=group_identifier)

    # definimos el formato de informacion a pasar
    context['group'] = [
        group_to_display.name,
        group_to_display.desc,
        group_to_display.user_balance(user_pk=user_to_work_with.primkey),
        # lista de las transacciones con info
        [],
    ]

    # cogemos todas las transacciones del grupo en las que esta metido el usuario
    transactions_of_user_in_group = group_to_display.transaction_set.filter(
        payers__primkey__contains=user_to_work_with.get_uidentifier()
    )

    for transaction in transactions_of_user_in_group:

        # lista de los nombres de los usuarios involucrados en la transaccion
        lista_nombres = []

        # cogemos a cada usuario y su rol en la transaccion (estado si es que ha pagado...)
        for payer in transaction.payers.all():
            payer_name = payer.django_user.username
            if transaction.get_score_role(payer.primkey) == 'OWNER':
                payer_name = payer_name + ' (OWNER)'
            elif transaction.get_score_role(payer.primkey) == 'DEBTER':
                if transaction.get_score_state(payer.primkey) == 'PAYED':
                    payer_name = payer_name + ' (PAYED)'
                elif transaction.get_score_state(payer.primkey) == 'NOTPAYED':
                    payer_name = payer_name + ' (OWS)'
            # añadimos ese nombre modificado en la lista de nombres para la transaccion
            lista_nombres.append(payer_name)

        # añadimos la info de cada transaccion a mostrar
        context['group'][3].append(
            [
                transaction.name,
                transaction.desc,
                transaction.total_price(),
                transaction.user_account(user_pk=user_to_work_with.primkey),
                lista_nombres,
                transaction.get_tridentifier(),
            ]
        )

    context['title'] = 'Group'
    context['nameClass'] = 'Group'
    context['username'] = user_to_work_with.django_user.username

    return render(request, 'applostickes/group.html', context)


@login_required
def createDebt(request):

    global user_to_work_with

    if user_to_work_with is None:
        user_to_work_with = User.objects.get(django_user__username=request.user.username)

    context = {}

    lista_peoples = []

    usergroup_tofilterwith = UserGroup.objects.filter(
        primkey__contains=applostickes.from_group_view_url_string.split('-')[1]
    )

    peoples_paying = User.objects.filter(
        usergroup__in=usergroup_tofilterwith
    )

    contador = 1
    for people in peoples_paying:
        lista_peoples.append([people.primkey, f'persona_{contador}', people.django_user.username])
        contador = contador + 1

    context['lista_peoples'] = lista_peoples

    form = TransactionForm(request.POST or None)

    if form.is_valid():

        todo_bien = True

        # el request.POST es un QueryDict, asi que vamos a dejarnos de tonterias y juguemos solo con el dict(),
        # hay que andarse con cuidado porque cada key tiene una LISTA de valores, aunque haya una sola cosa...
        request_as_dict = dict(request.POST)

        # creamos todos los elementos nuevos que el usuario ha querido añadir
        elementos_de_vue = []
        if 'elements_vue' in request_as_dict:
            for elemento in request_as_dict['elements_vue']:
                nombre_elemento = elemento.strip().split(' - ')[0]
                precio_elemento = int(elemento.strip().split(' - ')[1].split(' €')[0])
                element = Element(
                    name=nombre_elemento,
                    price=precio_elemento,
                )
                element.save()
                elementos_de_vue.append(element.primkey)

        """
            OBJETIVO -> generar un string tal que 1-1,2,3;2,3... a partir del request_as_dict

            si tenemos algo tal que
                payer = (numero)-
                payer_element_distribution = (numeros y comas y puntosycomas)

            el mapping final tendra la pinta de mapping = f'{payer}-{payer_element_distribution}'

            La cuestion es que la numeracion del string de mapping sigue la logica de "de todos los
            usuarios que pagan, el que paga es el ((n)-), numerando todos los usuarios que pagan de
            1 a m (1..m). Cada ";" significa uno de los elementos, y los numeros entre comas dicen
            los usuarios que han pagado ese elemento. De esta manera, "1-1,2;3,4" significa que los
            usuarios 1 y 2 comparten el elemento 1 de la compra, los usuarios 3 y 4 comparten el 
            elemento 2 de la compra y TODA la compra la paga el usuario 1 (no soportamos casos en 
            los que se comparten pagos a medias de la cuenta total, solo un alguien con los dineros 
            para pagar la cosa).

            La numeracion 1..m es de todos los usuarios involucrados en la compra, no necesariamente 
            todos los posibles usuarios que podrian haberse visto involucrados en la compra. Es decir,
            puede haber m usuarios en la transaccion de k usuarios totales registrados en el grupo 
            (such that m <= k) y estos pueden ser el primero del set total de usuarios del grupo, el 
            tercero, el decimoquinto y el trigesimocuarto usuarios del grupo (para un grupo con k > 
            34 usuarios, claro...). En cualquier caso, el primero, tercero, decimoquinto y 
            trigesimocuarto usuarios del grupo seran, respectivamente, el 1,2,3 y 4 de nuestro string 
            de mapping. El orden de estos usuarios viene definido por Django (forma bonita de decir 
            que no sabemos que criterio utiliza, asi que nos abstraemos de la fiesta esta) y es 
            constante en la definicion de objetos con esos valores (como las listas del diccionario 
            de request.POST, ejem ejem...), por lo que necesitamos extraer todos los usuarios 
            involucrados en la compra ORDENADOS tal y como vienen ordenados en el set total de 
            usuarios del grupo al cual pertenece la transaccion para poder hacer una correlacion 
            correcta de 1 -> primer_usuario, 2 -> tercer_usuario, 3 -> decimoquinto_usuario y 
            4 -> trigesimocuarto_usuario. Para ello, hacemos lo siguiente:

        """

        # comprobamos que todos los elementos de la transaccion tienen pagadores involucrados,
        # es decir, que hay el mimsmo numero de elementos en la lista de elementos que keys del tipo
        # "people_paying_element_X"...
        contador_listas_peoples = 0

        # extraemos las listas de usuarios involucrados en la compra
        dict_de_compradores = {}
        for key in request_as_dict.keys():
            if 'people_paying_element_' in key:
                contador_listas_peoples = contador_listas_peoples + 1
                dict_de_compradores[key] = request_as_dict[key]

        checkea_pagador_en_transaccion = True
        if 'elements' in request_as_dict and 'elements_vue' in request_as_dict:
            if (len(request_as_dict['elements']) + len(request_as_dict['elements_vue'])) != contador_listas_peoples:
                todo_bien = False
                checkea_pagador_en_transaccion = False
                form.add_error(
                    field='elements',
                    error=forms.ValidationError('Hay elementos sin usuarios checkeados.')
                )
        elif 'elements' in request_as_dict:
            if len(request_as_dict['elements']) != contador_listas_peoples:
                todo_bien = False
                checkea_pagador_en_transaccion = False
                form.add_error(
                    field='elements',
                    error=forms.ValidationError('Hay elementos sin usuarios checkeados.')
                )
        elif 'elements_vue' in request_as_dict:
            if len(request_as_dict['elements_vue']) != contador_listas_peoples:
                todo_bien = False
                checkea_pagador_en_transaccion = False
                form.add_error(
                    field='elements',
                    error=forms.ValidationError('Había elementos nuevos sin usuarios checkeados.')
                )
        else:
            todo_bien = False
            checkea_pagador_en_transaccion = False
            form.add_error(
                field='elements',
                error=forms.ValidationError('No has añadido ningún elemento a la transaccion.')
            )

        # obtenemos una lista de todos usuarios que pagan (repetidos)
        lista_de_todos_lospayers = []
        for key in dict_de_compradores.keys():
            lista_de_todos_lospayers.extend(dict_de_compradores[key])

        # eliminamos los duplicados (los sets en python son colecciones con esta propiedad)
        # no es necesario, pero las comprobaciones por "in" son mas rapidas con sets (me 
        # quiere sonar que lo lei en algun lado...)
        set_de_todos_lospayers = set(lista_de_todos_lospayers)

        # cogemos la lista de usuarios del grupo y los que no esten en el set los vamos quitando,
        # de tal forma que mantenemos el orden chachi que Django hace de los usuarios
        peoples_fromgroup_primkey_list = []
        for person_paying in peoples_paying:
            peoples_fromgroup_primkey_list.append(str(person_paying.primkey))

        peoples_paying_really = peoples_fromgroup_primkey_list.copy() # jejeeeee, cuidao que python a veces es gracioso
        for potential_payer in peoples_fromgroup_primkey_list:
            if potential_payer not in set_de_todos_lospayers:
                peoples_paying_really.remove(potential_payer)

        # comprobamos el caso erroneo en el que la transaccion solo pertenece a una persona (no nos interesa...)
        if len(peoples_paying_really) == 1:
            todo_bien = False
            form.add_error(
                field='elements',
                error=forms.ValidationError('No puedes tener un único usuario en la transaccion.')
            )

        # OJO al conjuro...
        #    >>> ','.join(sorted('3,2,1,'[0:(len('3,2,1,')-1)].split(',')))
        #    '1,2,3'

        # y ahora jugamos un poco con los indices
        payer_element_distribution = ''
        for key in dict_de_compradores.keys():
            element_distribution = ''
            for usuario_pagador in dict_de_compradores[key]:
                if usuario_pagador in peoples_paying_really:
                    element_distribution = element_distribution + f'{peoples_paying_really.index(usuario_pagador) + 1},'
            element_distribution = ','.join(sorted(element_distribution[0:(len(element_distribution)-1)].split(',')))
            payer_element_distribution = payer_element_distribution + element_distribution + ';'

        # quitamos el ultimo ';'
        payer_element_distribution = payer_element_distribution[0:(len(payer_element_distribution)-1)]

        """
            Ahora, para el encargado de pagar la cuenta, tenemos dos casos:
              (1) el que paga tiene cosas suyas en la cuenta
              (2) el que paga no tiene cosas suyas en la cuenta

            para el caso (1) solo con un .index() suficiente, en el caso (2) ponemos la
            primkey (sin '-', puestas como '#'...) como parte de 'payer' del 'mapping' y
            hacemos la gestion de eso ya bien en la funcion de accounts() de Transaction...

            DISCLAIMER:

            no consideramos el caso en el que un usuario que paga la transaccion no tiene 
            elementos suyos en la transaccion (se puede arreglar añadiendo un elemento de 
            0.01 € con vue supongo...)

        """

        payer = ''
        # ojo al tema de las listas, [0]...
        if request_as_dict['payer'][0] in peoples_paying_really:
            payer = str(peoples_paying_really.index(request_as_dict['payer'][0]) + 1)
        else:
            if checkea_pagador_en_transaccion:
                todo_bien = False
                form.add_error(
                    field='elements',
                    error=forms.ValidationError('El pagador no tiene nada en la transaccion.')
                )

        # string final
        mapping = f'{payer}-{payer_element_distribution}'

        if todo_bien:

            # empezamos a crear la transaccion porque todo ha ido super guay
            transaction_to_modify = form.save(commit=False)

            # save() necesario porque si no no puedes poner los atributos con FOREIGNKEYS y demasKEYS
            transaction_to_modify.save()

            # guardamos las referencias a los payers y elements necesarios
            transaction_to_modify.payers.set(User.objects.filter(primkey__in=peoples_paying_really)) # set() porque lo dice Django
            if 'elements' in request_as_dict:
                transaction_to_modify.elements.set(
                    Element.objects.filter(
                        primkey__in=request_as_dict['elements'] + elementos_de_vue
                    )
                ) # set() porque lo dice Django
            else:
                transaction_to_modify.elements.set(
                    Element.objects.filter(
                        primkey__in=elementos_de_vue
                    )
                ) # set() porque lo dice Django

            # definimos el mapping con lo generado anteriormente
            transaction_to_modify.mapping = mapping

            # ahora que tenemos los payers puestos, generamos el mapping de score_settling...
            transaction_to_modify.generate_score_settling_mapping()

            # save() para guardar los atributos de mapping y score_settling en tabla de DB
            transaction_to_modify.save()

            return redirect('debt', transaction_to_modify.name, transaction_to_modify.get_tridentifier())

    context['form'] = form
    context['title'] = 'Create debt'
    context['nameClass'] = 'Create debt'
    context['username'] = user_to_work_with.django_user.username
    context['group_name'] = applostickes.from_group_view_url_string.split('-')[0]
    context['groupIdentifier'] = applostickes.from_group_view_url_string.split('-')[1]

    return render(request, 'applostickes/createDebt.html', context)


@login_required
def debt(request, debtName, transaction_identifier):

    global user_to_work_with

    if user_to_work_with is None:
        user_to_work_with = User.objects.get(django_user__username=request.user.username)

    context = {}

    # cogemos la transaccion de identificador "transaction_identifier"
    transaction_to_display = Transaction.objects.get(primkey__contains=transaction_identifier)

    # definimos el formato de info a pasar
    context['debt'] = [
        transaction_to_display.user_group.name,
        transaction_to_display.user_group.get_ugidentifier(),
        transaction_to_display.name,
        transaction_to_display.desc,
        transaction_to_display.total_price(),
        transaction_to_display.user_account(user_pk=user_to_work_with.primkey),
        [],
        [],
        0,
        transaction_to_display.get_tridentifier()
    ]

    # cogemos a cada usuario y su rol en la transaccion (estado si es que ha pagado...)
    for payer in transaction_to_display.payers.all():
        payer_name = payer.django_user.username
        if transaction_to_display.get_score_role(payer.primkey) == 'OWNER':
            if payer_name == user_to_work_with.django_user.username:
                context['debt'][8] = 1 # el usuario es el OWNER de la deuda
            payer_name = payer_name + ' (OWNER)'
        elif transaction_to_display.get_score_role(payer.primkey) == 'DEBTER':
            if transaction_to_display.get_score_state(payer.primkey) == 'PAYED':
                payer_name = payer_name + ' (PAYED)'
            elif transaction_to_display.get_score_state(payer.primkey) == 'NOTPAYED':
                payer_name = payer_name + ' (OWS)'
        context['debt'][6].append(payer_name)

    # cogemos cada uno de los usuarios responsables de cada elemento y hacemos una
    # lista con sus nombres para displayearlos en el medio de la transaccion
    contador_mapping = 0
    for element in transaction_to_display.elements.all():

        # cogemos todos los numeros de pagadores (a la derecha del "-") del elemento
        # de la lista de indice [contador_mapping]
        nums_responsables = transaction_to_display.mapping.split("-")[1].split(";")[contador_mapping].split(",")

        # la lista de los nombres de los responsables para el elemento "element"
        # se llena con todos aquellos nombres de la lista de todos los usuarios
        # involucrados en la transaccion
        lista_responsables = []
        for num in nums_responsables:
            lista_responsables.append(context['debt'][6][int(num)-1])

        # metemos en una lista (1) el nombre del elemento sin el precio, (2) la lista de
        # responsables para ese elemento y (3) el precio de ese elemento
        context['debt'][7].append([element.name.split(" - ")[0], lista_responsables, element.price])

        # actualizamos el contador de elementos de la transaccion
        contador_mapping = contador_mapping + 1

    context['title'] = 'Debt'
    context['nameClass'] = 'Debt'
    context['username'] = user_to_work_with.django_user.username

    return render(request, 'applostickes/debt.html', context)


@login_required
def pay_debt(request, debt_identifier):

    global user_to_work_with

    if user_to_work_with is None:
        user_to_work_with = User.objects.get(django_user__username=request.user.username)

    # cogemos la transaccion que queremos pagar/marcar como pagada...
    transaction_to_work_with = Transaction.objects.get(primkey__contains=debt_identifier)

    # si el usuario loggeado es un pagador (debe pasta a alguien)
    if transaction_to_work_with.get_score_role(user_to_work_with.primkey) == 'DEBTER':
        # pues pagamos
        transaction_to_work_with.pay_transaction(user_to_work_with.primkey)

    # si el usuario loggeado es el dueño de la transaccion (le deben pasta)
    elif transaction_to_work_with.get_score_role(user_to_work_with.primkey) == 'OWNER':
        # que nos han pagado ya todos
        transaction_to_work_with.mark_as_payed()

    # si hemos venido desde debts
    if applostickes.debts_or_group_enter_point_to_debt_0_or_1 == 0:
        messages.success(request, 'Debt payed!')
        return redirect('debts')

    # si hemos venido desde group
    elif applostickes.debts_or_group_enter_point_to_debt_0_or_1 == 1:
        messages.success(request, 'Debt payed!')
        group_name = applostickes.from_group_view_url_string.split('-')[0]
        group_identifier = applostickes.from_group_view_url_string.split('-')[1]
        return redirect('group', group_name, group_identifier)

    # si ha pasado algo raro (refescos de pag o lo que sea...)
    else:
        messages.success(request, 'Debt payed!')
        return redirect('user')