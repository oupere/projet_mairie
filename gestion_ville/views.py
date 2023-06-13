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
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages





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