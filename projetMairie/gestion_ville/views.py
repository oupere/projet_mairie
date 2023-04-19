from django.shortcuts import render


def index(request):
    return render(request, 'accueil/index.html')

def services(request):
    return render(request, 'accueil/services.html')

def contact(request):
    return render(request, 'accueil/contact.html')

def team(request):
    return render(request, 'accueil/team.html')

def about(request):
    return render(request, 'accueil/about.html')


def publicite(request):
    return render(request, 'accueil/pub.html')


