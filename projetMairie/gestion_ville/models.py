from django.db import models

from django.utils import timezone
from django.contrib.gis.db import models


class Service(models.Model):
    nom = models.CharField(max_length=255)

class Citoyen(models.Model):
    nom = models.CharField(max_length=255)
    adresse = models.CharField(max_length=255)
    telephone = models.CharField(max_length=20)

class Employe(Citoyen):
    poste = models.CharField(max_length=255)
    date_naisse = models.DateField()
    salaire = models.PositiveIntegerField()
    
    def __str__(self):
        return f"Nom: {self.nom}   Role: {self.poste}"

class Signalement(models.Model):
    TYPES_SIGNALEMENT = (
        ('accident', 'Accident de la circulation'),
        ('nuisances', 'Nuisances sonores'),
        ('degradation', 'Dégradation des espaces publics'),
        ('eclairage', 'Pannes d\'éclairage public'),
        ('assainissement', 'Problèmes d\'assainissement'),
        ('graffiti', 'Tags et graffiti'),
        ('dechets', 'Dépôts sauvages de déchets'),
        ('infrastructures', 'Dommages aux infrastructures publiques'),
        ('vandalisme', 'Vandalisme'),
        ('stationnement', 'Problèmes de stationnement'),
    )
    description = models.TextField()
    date_signalement = models.DateTimeField(default=timezone.now)
    etat_signalement = models.CharField(max_length=50, default='en cours')
    lieu = models.CharField(max_length=100)
    type_signalement = models.CharField(max_length=20, choices=TYPES_SIGNALEMENT)
    location = models.PointField()
    citoyen = models.ForeignKey(Citoyen, on_delete=models.CASCADE, related_name='signalements')
    
    def __str__(self):
        return f"Signalement {self.pk}: {self.get_type_signalement_display()}"


from django.db import models

class Travail(models.Model):
    description = models.TextField()
    etat_davancement = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    signalements = models.ManyToManyField(Signalement, related_name='travaux')
    employes = models.ManyToManyField(Employe, related_name='travaux')

    def __str__(self):
        return f"Travail {self.pk}: {self.description}"

class Demande(models.Model):
    description = models.TextField()
    date_de_la_demande = models.DateField()
    etat_de_la_demande = models.CharField(max_length=255)
    cout = models.PositiveIntegerField()
    delai_traitement = models.CharField(max_length=255)
    numer_confirmation = models.CharField(max_length=255)
    citoyen = models.ForeignKey(Citoyen, on_delete=models.CASCADE, related_name='demandes')
