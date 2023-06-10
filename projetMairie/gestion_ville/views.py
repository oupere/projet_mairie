from django.shortcuts import render, redirect
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from geopy.geocoders import Nominatim
from .forms import SignalementForm 
from .models import Signalement
from django.utils import timezone
from django.shortcuts import render, get_object_or_404



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


""" def signalement(request):
    Signalemen_form = SignalemenForm(request.POST or None)
    form = SignalementForm(request.POST or None)
    if Signalemen_form.is_valid() and form.is_valid():
        Signalemen = Signalemen_form.save()
        signalement = form.save(commit=False)
        signalement.Signalemen = Signalemen
        geolocator = Nominatim(user_agent="gestion_ville")
        location = geolocator.geocode(signalement.lieu)
        if location:
            signalement.location = Point(location.longitude, location.latitude)
            signalement.save()
        return redirect('index') # rediriger vers une page de succès
        
    context = {
        'Signalemen_form': Signalemen_form,
        'form': form,
    }
    return render(request, 'signalement.html', context)
 """

from .widgets import SignalementForm, GoogleMapsPointWidget

def signalement(request):
    form = SignalementForm(request.POST or None)
    if form.is_valid():
        signalement = form.save(commit=False)
        geolocator = Nominatim(user_agent="gestion_ville")
        location = geolocator.geocode(signalement.lieu)
        if location:
            signalement.location = Point(location.longitude, location.latitude)
            signalement.save()
        return redirect('index')  
        
    context = {
        'form': form,
    }
    return render(request, 'signalement.html', context)



def liste_signalements(request):
    signalements = Signalement.objects.all()
    context = {'signalements': signalements}
    return render(request, 'liste_signalements.html', context)


def localiser(request, signalement_id):
    signalement = get_object_or_404(Signalement, pk=signalement_id)
    point = signalement.location
    print(point)
    latitude, longitude = point.coords
    context = {
        'default_lat': latitude,
        'default_lon': longitude,
        'signalement': signalement
    }
    return render(request, 'localiser.html', context)
