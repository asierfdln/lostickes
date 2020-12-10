from django.shortcuts import render
from django.http import HttpResponseRedirect
from django import forms
from .models import UserGroupForm, TransactionForm
from .models import User, UserGroup, Transaction, Element
import applostickes
# import pprint


userpks = {
    'user1': '7a8ae656-8b99-469d-a2b7-86774262b155',
    'user2': 'a80b2c81-0453-4acd-b5b5-26ae5b3ab16a',
    'user3': '85dbf8ed-98c7-477f-a396-9ff9d6b6a030',
    'user4': 'f7225a3d-7b47-4b43-b177-59cbb499958d',
}

user_to_work_with = None


def about(request):
    return render(request, 'applostickes/about.html', {'title': 'About'})


def main(request):
    return render(request, 'applostickes/main.html', {'title': 'Main'})


def user(request):

    global user_to_work_with

    user_to_work_with = User.objects.get(primkey=userpks['user2']) # TODO esto con la pagina de login

    context = {}

    groups_to_display = user_to_work_with.usergroup_set.all()
    context['groups'] = {}

    for group in groups_to_display:
        context['groups'][group.name] = group.user_balance(user_pk=user_to_work_with.primkey)

    transactions_to_display = user_to_work_with.transaction_set.all()
    context['transactions'] = {}

    for transaction in transactions_to_display:
        context['transactions'][transaction.name] = transaction.user_account(user_pk=user_to_work_with.primkey)

    context['title'] = 'User'
    context['nameClass'] = 'User'
    context['username'] = user_to_work_with.name

    return render(request, 'applostickes/user.html', context)


def groups(request):

    global user_to_work_with

    context = {}

    groups_to_display = user_to_work_with.usergroup_set.all()
    context['groups'] = {}

    for group in groups_to_display:

        context['groups'][group.name] = [
            group.desc,
            group.user_balance(user_pk=user_to_work_with.primkey),
            [],
            group.get_ugidentifier(),
        ]

        transactions_of_group = group.transaction_set.all()

        for tr in transactions_of_group:
            if tr.payers.get(primkey=user_to_work_with.primkey):
                context['groups'][group.name][2].append(
                    [
                        tr.name,
                        tr.user_account(user_pk=user_to_work_with.primkey)
                    ]
                )

    context['title'] = 'Groups'
    context['nameClass'] = 'Groups'
    context['username'] = user_to_work_with.name

    return render(request, 'applostickes/groups.html', context)


def debts(request):

    global user_to_work_with

    context = {}

    groups_of_user = user_to_work_with.usergroup_set.all()
    context['debts'] = {}

    for group in groups_of_user:

        transactions_of_group = group.transaction_set.all()

        for transaction in transactions_of_group:

            if transaction.payers.get(primkey=user_to_work_with.primkey):

                context['debts'][transaction.name] = [
                    transaction.desc,
                    group.name,
                    transaction.total_price(),
                    transaction.user_account(user_pk=user_to_work_with.primkey),
                    [],
                    transaction.get_tridentifier(),
                    group.get_ugidentifier(),
                ]

                transaction_accounts = transaction.accounts()

                for payer in transaction.payers.all():
                    payer_name = payer.name
                    if transaction_accounts[payer.primkey] < 0:
                        payer_name = payer_name + ' (OWNER)'
                    context['debts'][transaction.name][4].append(payer_name)

    context['title'] = 'Debts'
    context['nameClass'] = 'Debts'
    context['username'] = user_to_work_with.name

    return render(request, 'applostickes/debts.html', context)


def createGroup(request):

    global user_to_work_with

    context = {}

    form = UserGroupForm(request.POST or None)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/groups/')

    context['form'] = form
    context['title'] = 'Create group'
    context['nameClass'] = 'Create group'
    context['username'] = user_to_work_with.name

    return render(request, 'applostickes/createGroup.html', context)


def group(request, groupName, group_identifier):

    global user_to_work_with

    applostickes.from_group_to_createDebt_string = f'{groupName}-{group_identifier}'

    context = {}

    groups_of_user = user_to_work_with.usergroup_set.all()
    group_to_display = None

    for group in groups_of_user:
        if group_identifier in str(group.primkey):
            group_to_display = group
            break

    context['group'] = [
        group_to_display.name,
        group_to_display.desc,
        group_to_display.user_balance(user_pk=user_to_work_with.primkey),
        [],
    ]

    # ERROR ECUNTRADO PO IRH LOOOOOOOOOL VERIFICAR QUE PRIMKEY ESTA EN LA TRANSACCION
    # (no a este nivel, si no en user_balance, CRRRRRRRRREEEEEEOOOOOOOO)

    for transaction in group_to_display.transaction_set.all():

        lista_nombres = []
        transaction_accounts = transaction.accounts()

        for payer in transaction.payers.all():
            payer_name = payer.name
            if transaction_accounts[payer.primkey] < 0:
                payer_name = payer_name + ' (OWNER)'
            lista_nombres.append(payer_name)

        if user_to_work_with.name in lista_nombres or (user_to_work_with.name + ' (OWNER)') in lista_nombres:

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
    context['username'] = user_to_work_with.name

    return render(request, 'applostickes/group.html', context)


def createDebt(request):

    global user_to_work_with

    context = {}

    lista_peoples = []

    # if request.method != 'POST': # ESTE IF LLEGARIA HASTA LA LINEA DE 'context['lista_peoples'] = lista_peoples'
                                   # La razon por la que siempre cargamos la lista esta de peoples es que, si cometemos
                                   # algun fallo en el formulario y salta un ValidationError, tenemos que tener la lista
                                   # esa a mano...

    usergroup_tofilterwith = UserGroup.objects.filter(
        primkey__contains=applostickes.from_group_to_createDebt_string.split('-')[1]
    )

    peoples_paying = User.objects.filter(
        usergroup__in=usergroup_tofilterwith
    )

    contador = 1
    for people in peoples_paying:
        lista_peoples.append([people.primkey, f'people_{contador}', people.name]) # TODO @asier WTF primkey FORMS?!?!?!?!?!
        contador = contador + 1

    context['lista_peoples'] = lista_peoples

    form = TransactionForm(request.POST or None)

    if form.is_valid():

        # el request.POST es un QueryDict, asi que vamos a dejarnos de tonterias y juguemos solo con el dict(),
        # hay que andarse con cuidado porque cada key tiene una LISTA de valores, aunque haya una sola cosa...
        request_as_dict = dict(request.POST)

        # OBJETIVO -> generar un string tal que 1-1,2,3;2,3... a partir del request_as_dict
        #
        # si tenemos algo tal que
        #    payer = (numero)
        #    payer_element_distribution = (numeros y comas y puntosycomas)
        #
        # el mapping final tendra la pinta de mapping = f'{payer}-{payer_element_distribution}'

        # La cuestion es que la numeracion del string de mapping sigue la logica de "de todos los
        # usuarios que pagan, el que paga es el ((n)-), numerando todos los usuarios que pagan de
        # 1 a m (1..m). Cada ";" significa uno de los elementos, y los numeros entre comas dicen
        # los usuarios que han pagado ese elemento. De esta manera, "1-1,2;3,4" significa que los
        # usuarios 1 y 2 comparten el elemento 1 de la compra, los usuarios 3 y 4 comparten el 
        # elemento 2 de la compra y TODA la compra la paga el usuario 1 (no soportamos casos en 
        # los que se comparten pagos a medias de la cuenta total, solo un alguien con los dineros 
        # para pagar la cosa).
        #
        # La numeracion 1..m es de todos los usuarios involucrados en la compra, no necesariamente 
        # todos los posibles usuarios que podrian haberse visto involucrados en la compra. Es decir,
        # puede haber m usuarios en la transaccion de k usuarios totales registrados en el grupo 
        # (such that m <= k) y estos pueden ser el primero del set total de usuarios del grupo, el 
        # tercero, el decimoquinto y el trigesimocuarto usuarios del grupo (para un grupo con k > 
        # 34 usuarios, claro...). En cualquier caso, el primero, tercero, decimoquinto y 
        # trigesimocuarto usuarios del grupo seran, respectivamente, el 1,2,3 y 4 de nuestro string 
        # de mapping. El orden de estos usuarios viene definido por Django (forma bonita de decir 
        # que no sabemos que criterio utiliza, asi que nos abstraemos de la fiesta esta) y es 
        # constante en la definicion de objetos con esos valores (como las listas del diccionario 
        # de request.POST, ejem ejem...), por lo que necesitamos extraer todos los usuarios 
        # involucrados en la compra ORDENADOS tal y como vienen ordenados en el set total de 
        # usuarios del grupo al cual pertenece la transaccion para poder hacer una correlacion 
        # correcta de 1 -> primer_usuario, 2 -> tercer_usuario, 3 -> decimoquinto_usuario y 
        # 4 -> trigesimocuarto_usuario. Para ello, hacemos lo siguiente:

        # extraemos las listas de usuarios involucrados en la compra
        dict_de_elementos = {}
        for key in request_as_dict.keys():
            if 'people_paying_element_' in key:
                dict_de_elementos[key] = request_as_dict[key]

        # obtenemos una lista de todos usuarios que pagan (repetidos)
        lista_de_todos_lospayers = []
        for key in dict_de_elementos.keys():
            lista_de_todos_lospayers.extend(dict_de_elementos[key])

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

        # OJO al conjuro...
        #    >>> ','.join(sorted('3,2,1,'[0:(len('3,2,1,')-1)].split(',')))
        #    '1,2,3'

        # y ahora jugamos un poco con los indices
        payer_element_distribution = ''
        for key in dict_de_elementos.keys():
            element_distribution = ''
            for usuario_pagador in dict_de_elementos[key]:
                if usuario_pagador in peoples_paying_really:
                    element_distribution = element_distribution + f'{peoples_paying_really.index(usuario_pagador) + 1},'
            element_distribution = ','.join(sorted(element_distribution[0:(len(element_distribution)-1)].split(',')))
            payer_element_distribution = payer_element_distribution + element_distribution + ';'

        # quitamos el ultimo ';'
        payer_element_distribution = payer_element_distribution[0:(len(payer_element_distribution)-1)]

        # ahora, para el encargado de pagar la cuenta, tenemos dos casos:
        #   (1) el que paga tiene cosas suyas en la cuenta
        #   (2) el que paga no tiene cosas suyas en la cuenta
        # 
        # para el caso (1) solo con un .index() suficiente, en el caso (2) ponemos la
        # primkey (sin '-', puestas como '#'...) como parte de 'payer' del 'mapping' y
        # hacemos la gestion de eso ya bien en la funcion de accounts() de Transaction...

        payer = ''
        # ojo al tema de las listas, [0]...
        if request_as_dict['payer'][0] in peoples_paying_really:
            payer = str(peoples_paying_really.index(request_as_dict['payer'][0]) + 1)
        else:
            payer = request_as_dict['payer'][0].replace('-', '#')

        # string final
        mapping = f'{payer}-{payer_element_distribution}'

        transaction_to_modify = form.save(commit=False)
        transaction_to_modify.mapping = mapping
        transaction_to_modify.usergroup = usergroup_tofilterwith[0]

        transaction_to_modify.save()

        transaction_to_modify.payers.set(User.objects.filter(primkey__in=peoples_paying_really)) # set() porque lo dice Django
        transaction_to_modify.elements.set(Element.objects.filter(primkey__in=request_as_dict['elements'])) # set() porque lo dice Django

        return HttpResponseRedirect(f'/group/{applostickes.from_group_to_createDebt_string}')

    context['form'] = form
    context['title'] = 'Create group'
    context['nameClass'] = 'Create group'
    context['username'] = user_to_work_with.name

    return render(request, 'applostickes/createDebt.html', context)


def debt(request, debtName, transaction_identifier):

    global user_to_work_with

    context = {}

    groups_of_user = user_to_work_with.usergroup_set.all()
    transaction_to_display = None

    for group in groups_of_user:
        for transaction in group.transaction_set.all():
            if transaction_identifier in str(transaction.primkey):
                transaction_to_display = transaction
                break

    context['debt'] = [
        transaction_to_display.user_group.name,
        transaction_to_display.user_group.get_ugidentifier(),
        transaction_to_display.name,
        transaction_to_display.desc,
        transaction_to_display.total_price(),
        transaction_to_display.user_account(user_pk=user_to_work_with.primkey),
        [],
        [],
    ]

    transaction_accounts = transaction.accounts()

    for payer in transaction_to_display.payers.all():
        payer_name = payer.name
        if transaction_accounts[payer.primkey] < 0:
            payer_name = payer_name + ' (OWNER)'
        context['debt'][6].append(payer_name)

    contador_mapping = 0

    for element in transaction_to_display.elements.all():

        nums_responsables = transaction_to_display.mapping.split("-")[1].split(";")[contador_mapping].split(",")
        lista_responsables = []

        for num in nums_responsables:
            lista_responsables.append(context['debt'][6][int(num)-1])

        context['debt'][7].append([element.name, lista_responsables, element.price])
        contador_mapping = contador_mapping + 1

    context['title'] = 'Debt'
    context['nameClass'] = 'Debt'
    context['username'] = user_to_work_with.name

    return render(request, 'applostickes/debt.html', context)
