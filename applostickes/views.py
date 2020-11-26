from django.shortcuts import render

posts = [
    {
        'author': 'CoreyMS',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'August 27, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'August 28, 2018'
    }
]

def home(request):
    context = {
        'posts': posts
    }
    return render(request, 'applostickes/home.html', context)

def about(request):
    return render(request, 'applostickes/about.html', {'title': 'About'})

def main(request):
    return render(request, 'applostickes/main.html', {'title': 'Main'})

def user(request):
    return render(request, 'applostickes/user.html', {'title': 'User'})

def group(request):
    context = {
        'posts': posts
    }
    return render(request, 'applostickes/group.html', context)

def debt(request):
    context = {
        'posts': posts
    }
    return render(request, 'applostickes/debt.html', context)

def createGroup(request):
    return render(request, 'applostickes/createGroup.html')