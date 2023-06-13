from django.shortcuts import render, redirect
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from geopy.geocoders import Nominatim
from .forms import SignalementForm, DemandeForm, CitoyenForm
from .models import Signalement, Demande, Citoyen
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from .widgets import SignalementForm, GoogleMapsPointWidget
from datetime import date, datetime




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

def create_demande(request):
    citoyens = Citoyen.objects.all()
    
    if request.method == 'POST':
        form = DemandeForm(request.POST, request.FILES)
        if form.is_valid():
            demande = form.save(commit=False)
            nom = request.POST.get('nom')
            prenom = request.POST.get('prenom')
            telephone = request.POST.get('telephone')
            adresse = request.POST.get('adresse')
            try:
                citoyen = Citoyen.objects.get(nom=nom, prenom=prenom, telephone=telephone)
            except citoyen.DoesNotExist:
                citoyen = Citoyen(nom=nom, prenom=prenom, telephone=telephone, adresse=adresse)
                print(citoyen)
                citoyen.save()
            demande.citoyen = citoyen
            demande.date = date.today()
            demande.type = request.POST.get('type')
            demande.recup = form.cleaned_data['recup']
            if demande.recup:
                if request.POST.get('type') == 'administratif':
                    demande.cout = 2500
                else:
                    demande.cout = 2000
            else:
                if request.POST.get('type') == 'administratif':
                    demande.cout = 2000
                else:
                    demande.cout = 1500
            demande. delai_traitement = '24hr'
            demande.etat = "Non traité"
            maintenant = datetime.now()
            demande.confirm = f"0112{prenom[:2]}{maintenant.strftime('%H%M%S%f')}{nom[:2]}2002"

            demande.save()
            return render(request, 'forms/confirm_demande.html', {'numero': demande.confirm})
    else:
        form = DemandeForm()
    return render(request, 'forms/create-demande.html', {'form': form, 'citoyens': citoyens})

def suivi(request):
    if request.method == 'POST':
        numero_confirmation = request.POST['numero_confirmation']
        demande = Demande.objects.filter(confirm=numero_confirmation).first()
        if demande:
            etat = demande.etat
            print(etat)
            valft = demande.fichier_telecharge
            print(valft)
            if valft:
                print("ici cest deja tlchargé")
                return render(request, 'forms/suivi_demande.html', {'demande': demande, 'valft': valft})
            else:
                if demande.etat == "Traité":
                    print("dans le false")
                    demande.fichier_telecharge = True
                    demande.save()
                    return render(request, 'forms/suivi_demande.html', {'etat': etat, 'demande': demande, 'fichier_telecharge': valft})
        else:
            ntrouve = "Aucune demande trouvée avec ce numéro de confirmation."
            return render(request, 'forms/suivi_demande.html', {'ntrouve': ntrouve})
    return render(request, 'forms/suivi_demande.html')

def demandes(request):
    demandes = Demande.objects.all()
    return render(request, 'forms/liste_demande.html', {'demandes': demandes})

def modifier_demande(request, demande_id):
    demande = get_object_or_404(Demande, id=demande_id)
    if request.method == 'POST':
        #form = DemandeForm(request.POST, request.FILES, instance=demande)
        if demande.recup:
            if 'filerecup' in request.FILES:
                demande.filerecup = request.FILES['filerecup']
                demande.etat = request.POST.get('etat')
                demande.save()
        else:
            demande.etat = request.POST.get('etat')
            demande.save()
        print("on redirige non")
        return redirect('demandes')
    return render(request, 'forms/modifier_demande.html', {'demande': demande})