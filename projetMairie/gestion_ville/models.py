from django.db import models

from django.utils import timezone

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

from django.contrib.gis.db import models

class Signalement(models.Model):
    TYPES_SIGNALEMENT = (
        ('type1', 'Type 1'),
        ('type2', 'Type 2'),
        ('type3', 'Type 3'),
    )
    description = models.TextField()
    date_signalement = models.DateTimeField(default=timezone.now)
    etat_signalement = models.CharField()
    lieu = models.CharField()
    type_signalement = models.CharField(max_length=20, choices=TYPES_SIGNALEMENT)
    location = models.PointField()
    citoyen = models.ForeignKey(Citoyen, on_delete=models.CASCADE, related_name='signalements')

class Travail(models.Model):
    description = models.TextField()
    date_debut = models.DateField()
    date_fin_prevue = models.DateField()
    etat_davancement = models.PositiveIntegerField()
    signalements = models.ManyToManyField(Signalement, related_name='travaux')
    employes = models.ManyToManyField(Employe, related_name='travaux')

class Demande(models.Model):
    description = models.TextField()
    date_de_la_demande = models.DateField()
    etat_de_la_demande = models.CharField(max_length=255)
    cout = models.PositiveIntegerField()
    delai_traitement = models.CharField(max_length=255)
    numer_confirmation = models.CharField(max_length=255)
    citoyen = models.ForeignKey(Citoyen, on_delete=models.CASCADE, related_name='demandes')
