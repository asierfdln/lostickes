from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import UserGroupForm, TransactionForm
from .models import User, Transaction

posts = [
    {
        'groupName': 'Group 1',
        'description': 'This group was created for Italy trip',
        'balance': '80',
        'debt': 'Debt 1',
        'debtBalance': '2'
    },
    {
        'groupName': 'Group 2',
        'description': 'This group was created for USA trip',
        'balance': '180',
        'debt': 'Debt 1',
        'debtBalance': '50'
    },
    {
        'groupName': 'Group 3',
        'description': 'This group was created for France trip',
        'balance': '200',
        'debt': 'Debt 1',
        'debtBalance': '12'
    }
]

postsDebt = [
    {
        'debtName': 'Debt 1',
        'description': 'This group was created for Italy trip',
        'groupName': 'Group 1',
        'cost': '30',
        'debtBalance': '2',
        'user1': 'user 1',
        'user2': 'user 2',
        'user3': 'user 3',
        'user4': 'user 4',
    },
    {
        'debtName': 'Debt 2',
        'description': 'This group was created for Italy trip',
        'groupName': 'Group 1',
        'cost': '20',
        'debtBalance': '29',
        'user1': 'user 1',
        'user2': 'user 2',
        'user3': 'user 3',
        'user4': 'user 4',
    },
    {
        'debtName': 'Debt 3',
        'description': 'This group was created for Italy trip',
        'groupName': 'Group 2',
        'cost': '80',
        'debtBalance': '0',
        'user1': 'user 1',#hay que hacerlo con una lista pero esto es una prueba
        'user2': 'user 2',
        'user3': 'user 3',
        'user4': 'user 4',
    }
    
]

USER = "user2" # simulacion de inicio de sesion

def about(request):
    return render(request, 'applostickes/about.html', {'title': 'About'})


def main(request):
    return render(request, 'applostickes/main.html', {'title': 'Main'})


def user(request):
    context = {}

    groups_to_display = User.objects.get(name=USER).usergroup_set.all()
    context['groups'] = {}
    for group in groups_to_display:
        context['groups'][group.name] = group.user_balance(user=USER)

    transactions_to_display = User.objects.get(name=USER).transaction_set.all()
    context['transactions'] = {}
    for transaction in transactions_to_display:
        context['transactions'][transaction.name] = transaction.user_account(user=USER)

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
    context = {
        'posts': groupName,
        'info': postsDebt,
        'nameClass': 'Group',
        'title': 'Group'
    }

    return render(request, 'applostickes/group.html', context)


def createDebt(request, goback_group):
    context = {}

    form = TransactionForm(request.POST)
    if form.is_valid():
        # comprobaciones logicas
        form.save()
        return HttpResponseRedirect(f'/group/{goback_group}')

    context['form'] = form
    context['title'] = 'Create group'
    context['nameClass'] = 'Create group'

    return render(request, 'applostickes/createDebt.html', context)

def debt(request, debtName):
    context = {
        'posts': debtName,
        'info': postsDebt,
        'nameClass': 'Debt',
        'title': 'Debt'
    }

    return render(request, 'applostickes/debt.html', context)