from django.shortcuts import render

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

def about(request):
    return render(request, 'applostickes/about.html', {'title': 'About'})

def main(request):
    return render(request, 'applostickes/main.html', {'title': 'Main'})

def user(request):
    return render(request, 'applostickes/user.html', {'title': 'User'})

def groups(request):
    context = {
        'posts': posts,
        'title': "Groups"
    }
    return render(request, 'applostickes/groups.html', context)

def debts(request):
    context = {
        'posts': postsDebt,
        'title': "Debts"
    }
    return render(request, 'applostickes/debts.html', context)

def createGroup(request):
    return render(request, 'applostickes/createGroup.html', {'title': 'Create group'})