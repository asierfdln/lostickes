from django.shortcuts import render
# from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django import forms
import applostickes
from .models import UserGroupForm, TransactionForm
from .models import User, UserGroup, Transaction


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

    user_to_work_with = User.objects.get(primkey=userpks['user1']) # TODO esto con la pagina de login

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

    return render(request, 'applostickes/debts.html', context)


def createGroup(request):

    context = {}

    form = UserGroupForm(request.POST) # TODO @asier creo que es esto lo que falla y da todos los errores de formulario

    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/groups/')
        # return redirect('place') # TODO @asier

    context['form'] = form
    context['title'] = 'Create group'
    context['nameClass'] = 'Create group'

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

    for transaction in group_to_display.transaction_set.all():

        lista_nombres = []
        transaction_accounts = transaction.accounts()

        for payer in transaction.payers.all():
            payer_name = payer.name
            if transaction_accounts[payer.primkey] < 0:
                payer_name = payer_name + ' (OWNER)'
            lista_nombres.append(payer_name)

        if user_to_work_with.name in lista_nombres:

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

    return render(request, 'applostickes/group.html', context)


def createDebt(request):

    global user_to_work_with

    context = {}

    lista_peoples = []

    if request.method != 'POST':

        peoples_paying = User.objects.filter(
            usergroup__in=UserGroup.objects.filter(
                primkey__contains=applostickes.from_group_to_createDebt_string.split('-')[1]
            )
        )

        contador = 1
        for people in peoples_paying:
            lista_peoples.append([people.primkey, f'people_{contador}', people.name]) # TODO @asier WTF primkey FORMS?!?!?!?!?!
            contador = contador + 1

        context['lista_peoples'] = lista_peoples

    form = TransactionForm(request.POST or None)

    print('wasa<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
    print(request.POST)

    if form.is_valid():
        user_group_object = form.cleaned_data['user_group']
        payers_object = form.cleaned_data['payers']

        # CTRL + D HERE SON (1)
        # transaction_to_modify = form.save(commit=False)
        # transaction_to_modify.mapping = CTRL + D HERE SON

        string_grupo = user_group_object.name
        booleano_payers_dentro = True

        for payer in payers_object:

            booleano_usergroup_encontrado = False

            for usergroup in payer.usergroup_set.all():
                if string_grupo == usergroup.name:
                    booleano_usergroup_encontrado = True
                    break
                else:
                    pass

            if not booleano_usergroup_encontrado:
                booleano_payers_dentro = False
                break

        if not booleano_payers_dentro:
            form.add_error(
                field='payers',
                error=forms.ValidationError('Hay usuario/s pagadores que no estan en el grupo de la transaccion.')
            )
        else:
            # CTRL + D HERE SON (1)
            # ver https://docs.djangoproject.com/en/3.0/topics/forms/modelforms/#the-save-method
            # ver https://cdf.9vo.lt/3.0/django.forms.models/ModelForm.html#save
            # transaction_to_modify.save()
            # form.save_m2m()
            form.save()
            return HttpResponseRedirect(f'/group/{applostickes.from_group_to_createDebt_string}')
            # return redirect('place') # TODO @asier

    context['form'] = form
    context['title'] = 'Create group'
    context['nameClass'] = 'Create group'

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

    return render(request, 'applostickes/debt.html', context)