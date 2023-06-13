from django.shortcuts import render, redirect
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from geopy.geocoders import Nominatim
from .forms import SignalementForm, CitoyenForm, TravailForm
from .models import Employe, Signalement, Travail
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages



def index(request):
    return render(request, 'accueil/index.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)  
            return redirect('dashboard')  
        else:
            messages.error(request, "Échec de la connexion. Veuillez vérifier vos informations d'identification.")
    
    return render(request, 'authentification/login.html')





def logout(request):
    logout(request)
    return redirect('login')



def dashboard(request):
    
    
    return render(request, 'authentification/dashboard.html')



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

#from .widgets import SignalementForm, CitoyenForm,  GoogleMapsPointWidget

from django.contrib.gis.geos import Point
from shapely.geometry import shape
from shapely.wkt import loads as load_wkt


from django.contrib.gis.geos import Point
from shapely.wkt import loads as load_wkt

# ...

""" def signalement(request):
    citoyen_form = CitoyenForm(request.POST or None)
    form = SignalementForm(request.POST or None)
    location = None  # Initialiser la variable location à None

    if request.method == 'POST':

        geolocator = Nominatim(user_agent="gestion_ville")
        location = geolocator.geocode(form.data.get('lieu'))
    if location:
        point = Point(location.longitude, location.latitude)
        wkt = point.wkt
        form_data = form.data.copy()  # Créer une copie modifiable des données du formulaire
        form.initial['location'] = wkt  # Modifier la copie des données du formulaire

        # Créer un nouveau formulaire avec les données modifiées
        form = SignalementForm(form_data)

    if citoyen_form.is_valid() and form.is_valid():
        citoyen = citoyen_form.save()
        signalement = form.save(commit=False)
        signalement.citoyen = citoyen
        signalement.location = load_wkt(form.cleaned_data['location'])
        signalement.save()
        return redirect('index')  # Rediriger vers une page de succès


    context = {
        'citoyen_form': citoyen_form,
        'form': form,
    }
    return render(request, 'signalement.html', context) """
    
def signalement(request):
    citoyen_form = CitoyenForm(request.POST or None)
    form = SignalementForm(request.POST or None)
    location = None  # Initialiser la variable location à None

    if request.method == 'POST':
        geolocator = Nominatim(user_agent="gestion_ville")
        location = geolocator.geocode(form.data.get('lieu'))

    if location:
        point = Point(location.longitude, location.latitude)
        form_data = form.data.copy()
        form_data['longitude'] = point.x
        form_data['latitude'] = point.y
        form = SignalementForm(form_data)

    if citoyen_form.is_valid() and form.is_valid():
        citoyen = citoyen_form.save()
        signalement = form.save(commit=False)
        signalement.citoyen = citoyen
        signalement.save()
        return redirect('index')

    context = {
        'citoyen_form': citoyen_form,
        'form': form,
    }
    return render(request, 'signalement.html', context)


def liste_signalements(request):
    signalements = Signalement.objects.all()
    context = {'signalements': signalements}
    return render(request, 'signalement/list_signalement.html', context)



def signalement_detail(request, signalement_id):
    signalement = Signalement.objects.get(pk=signalement_id)
    citoyen = signalement.citoyen
    context = {
        'signalement': signalement,
        'citoyen': citoyen,
    }
    return render(request, 'signalement/detail_signalement.html', context)

from django.shortcuts import get_object_or_404, redirect, render
from .forms import SignalementForm

""" def update_signalement(request, signalement_id):
    signalement = get_object_or_404(Signalement, pk=signalement_id)

    if request.method == 'POST':
        form = SignalementForm(request.POST, instance=signalement)
        if form.is_valid():
            form.save()
            return redirect('detail_signalement', signalement_id=signalement_id)  # Rediriger vers la page des détails du signalement

    else:
        form = SignalementForm(instance=signalement)

    context = {
        'signalement': signalement,
        'form': form,
    }
    return render(request, 'update_signalement.html', context)

 """
 
def creer_travail(request, signalement_id):
    signalement = get_object_or_404(Signalement, pk=signalement_id)

    if request.method == 'POST':
        form = TravailForm(request.POST)
        if form.is_valid():
            travail = form.save(commit=False)
            travail.etat_davancement = 0  # Initialiser l'état d'avancement à 0%
            travail.save()

            employe_ids = request.POST.getlist('employes')  # Récupérer les identifiants des employés sélectionnés dans le formulaire
            employes = Employe.objects.filter(id__in=employe_ids)  # Récupérer les objets Employe correspondant aux identifiants
            travail.employes.set(employes)  # Assigner les employés au travail

            travail.signalements.add(signalement)  # Associer le signalement au travail

            return redirect('detail_travail', travail_id=travail.id)  # Rediriger vers la page des détails du travail
    else:
        form = TravailForm()

    employes = Employe.objects.all()
    context = {
        'signalement': signalement,
        'form': form,
        'employes': employes,
    }
    return render(request, 'travail/create_travail.html', context)



def liste_travaux(request):
    travaux = Travail.objects.all()
    
    context = {
        'travaux': travaux,
    }
    
    return render(request, 'travail/liste_travaux.html', context)


def detail_travail(request, travail_id):
    travail = get_object_or_404(Travail, id=travail_id)
    signalements = travail.signalements.all()
    
    context = {
        'travail': travail,
        'signalements': signalements,
    }
    
    return render(request, 'travail/detail_travail.html', context)



""" def update_travail(request, travail_id):
    travail = get_object_or_404(Travail, id=travail_id)
    
    if request.method == 'POST':
        form = TravailForm(request.POST, instance=travail)
        if form.is_valid():
            form.save()
            return redirect('detail_travail', travail_id=travail_id)
    else:
        form = TravailForm(instance=travail)
    
    context = {
        'form': form,
        'travail': travail,
    }
    
    return render(request, 'travail/update_travail.html', context)
 """
 
def update_travail(request, travail_id):
    travail = get_object_or_404(Travail, id=travail_id)
    
    if request.method == 'POST':
        form = TravailForm(request.POST, instance=travail)
        if form.is_valid():
            travail = form.save(commit=False)
            
            # Récupérer les employés sélectionnés
            employe_ids = request.POST.getlist('employes')
            employes = Employe.objects.filter(id__in=employe_ids)
            
            # Associer les employés au travail
            travail.employes.set(employes)
            
            travail.save()
            
            return redirect('detail_travail', travail_id=travail_id)
    else:
        form = TravailForm(instance=travail)
    
    # Récupérer les employés associés au travail
    selected_employes = travail.employes.all()
    
    context = {
        'form': form,
        'travail': travail,
        'selected_employes': selected_employes,  # Ajouter la liste des employés sélectionnés au contexte
    }
    
    return render(request, 'travail/update_travail.html', context)



def supprimer_signalement(request, signalement_id):
    signalement = get_object_or_404(Signalement, pk=signalement_id)
    citoyen = signalement.citoyen

    if request.method == 'POST':
        # Supprimer le signalement et le citoyen
        signalement.delete()
        citoyen.delete()
        return redirect('index')  # Rediriger vers une page appropriée après la suppression

    context = {
        'signalement': signalement,
        'citoyen': citoyen,
    }
    return render(request, 'signalement/delete_signalement.html', context)




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
    print(context)
    return render(request, 'signalement/localiser.html', context)