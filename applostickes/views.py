from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.forms import ValidationError
from .models import UserGroupForm, TransactionForm
from .models import User, UserGroup, Transaction


USER = "user2" # simulacion de inicio de sesion

userpks = {
    'user1': '7a8ae656-8b99-469d-a2b7-86774262b155',
    'user2': 'a80b2c81-0453-4acd-b5b5-26ae5b3ab16a',
    'user3': '85dbf8ed-98c7-477f-a396-9ff9d6b6a030',
    'user4': 'f7225a3d-7b47-4b43-b177-59cbb499958d',
}

def about(request):
    return render(request, 'applostickes/about.html', {'title': 'About'})


def main(request):
    return render(request, 'applostickes/main.html', {'title': 'Main'})


def user(request): # TODO eliminar barra del final de los cuadradicos
    context = {}

    user_to_work_with = User.objects.get(primkey=userpks['user2']) # TODO esto con la pagina de login y una 'global' ezpz

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

    return render(request, 'applostickes/user.html', context)


def groups(request):
    context = {}

    groups_to_display = User.objects.get(name=USER).usergroup_set.all()
    context['groups'] = {}
    for group in groups_to_display:
        context['groups'][group.name] = [group.desc, group.user_balance(user=USER), []]
        transactions_of_group = group.transaction_set.all()
        for tr in transactions_of_group:
            if tr.payers.get(name=USER):
                context['groups'][group.name][2].append([tr.name, tr.user_account(user=USER)])

    context['title'] = 'Groups'
    context['nameClass'] = 'Groups'

    return render(request, 'applostickes/groups.html', context)


def debts(request):
    context = {}

    groups_of_user = User.objects.get(name=USER).usergroup_set.all()
    context['debts'] = {}
    for group in groups_of_user:
        transactions_of_group = group.transaction_set.all()
        for tr in transactions_of_group:
            if tr.payers.get(name=USER):
                context['debts'][tr.name] = [tr.desc, group.name, tr.total_price(), tr.user_account(user=USER), []]
                for user in tr.payers.all():
                    context['debts'][tr.name][4].append(user.name)

    context['title'] = 'Debts'
    context['nameClass'] = 'Debts'

    return render(request, 'applostickes/debts.html', context)


def createGroup(request):
    context = {}

    form = UserGroupForm(request.POST)
    if form.is_valid():
        # comprobaciones logicas
        form.save()
        return HttpResponseRedirect('/groups/')

    context['form'] = form
    context['title'] = 'Create group'
    context['nameClass'] = 'Create group'

    return render(request, 'applostickes/createGroup.html', context)


def group(request, groupName):
    context = {}

    group = UserGroup.objects.get(name=groupName) # TODO con primkey
    context['group'] = [group.name, group.desc, group.user_balance(user=USER), []]
    for transaction in group.transaction_set.all():
        lista_nombres = []
        for payer in transaction.payers.all():
            lista_nombres.append(payer.name)
        if USER in lista_nombres:
            context['group'][3].append([transaction.name, transaction.desc, transaction.total_price(), transaction.user_account(user=USER), lista_nombres])

    context['title'] = 'Group'
    context['nameClass'] = 'Group'

    return render(request, 'applostickes/group.html', context)


# TODO volver al group/{gruponame}
def createDebt(request): # (request, gruponame)
    context = {}

    form = TransactionForm(request.POST)
    if form.is_valid():
        # comprobaciones logicas
        user_group_object = form.cleaned_data['user_group']
        payers_object = form.cleaned_data['payers']

        string_grupo = user_group_object.name

        booleano_payers_dentro = True
        for payer in payers_object:
            booleano_usergroup_encontrado = False
            for usergroup in payer.usergroup_set.all():
                if string_grupo == usergroup.name:
                    # usuario correcto
                    booleano_usergroup_encontrado = True
                    break
                else:
                    # usuario de momento no correcto, hay que seguir mirando
                    pass
            if not booleano_usergroup_encontrado:
                booleano_payers_dentro = False
                break

        if not booleano_payers_dentro:
            form.add_error(
                field='payers',
                error=ValidationError("Hay usuario/s pagadores que no estan en el grupo de la transaccion.")
            )
        else:
            form.save()
            return HttpResponseRedirect(f'/debts/') # f'/group/{gruponame}'

    context['form'] = form
    context['title'] = 'Create group'
    context['nameClass'] = 'Create group'

    return render(request, 'applostickes/createDebt.html', context)


def debt(request, debtName):
    context = {}

    trani = Transaction.objects.get(name=debtName) # TODO con primkey
    context['debt'] = [trani.user_group.name, trani.name, trani.desc, trani.total_price(), trani.user_account(user=USER)]
    lista_nombres = []
    for payer in trani.payers.all():
        lista_nombres.append(payer.name)
    context['debt'].append(lista_nombres)
    context['debt'].append([])
    contador_mapping = 0
    for element in trani.elements.all():
        nums_responsables = trani.mapping.split(";")[contador_mapping].split(",")
        lista_responsables = []
        for num in nums_responsables:
            lista_responsables.append(lista_nombres[int(num)-1])
        context['debt'][6].append([element.name, lista_responsables, element.price])
        contador_mapping = contador_mapping + 1

    context['title'] = 'Debt'
    context['nameClass'] = 'Debt'

    return render(request, 'applostickes/debt.html', context)