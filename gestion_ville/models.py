from django.db import models
from django.utils import timezone
import os
from django.core.exceptions import ValidationError
from django.contrib.gis.db import models

class Service(models.Model):
    nom = models.CharField(max_length=255)

class Citoyen(models.Model):
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    adresse = models.CharField(max_length=255)
    telephone = models.CharField(max_length=20)
    
    def __str__(self):
        return self.nom + " " + self.prenom


class Employe(Citoyen):
    poste = models.CharField(max_length=255)
    date_naisse = models.DateField()
    salaire = models.PositiveIntegerField()

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

def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # Récupérer l'extension du fichier
    valid_extensions = ['.pdf', '.png', '.jpg', '.jpeg', '.webp']
    if ext.lower() not in valid_extensions:
        raise ValidationError('Seuls les fichiers PDF et les images (png, jpg, jpeg) sont autorisés.')

class Demande(models.Model):
    type = models.TextField()
    date = models.DateField(blank=True)
    etat = models.CharField(blank=True)
    cout = models.PositiveIntegerField(blank=True)
    delai_traitement = models.CharField(blank=True)
    confirm = models.CharField(blank=True)
    citoyen = models.ForeignKey(Citoyen, on_delete=models.CASCADE, related_name='demandes', blank=True)
    fichier = models.FileField(upload_to='demande_files/', validators=[validate_file_extension])
    recup = models.BooleanField(default=False)
    filerecup = models.FileField(upload_to='recup/', blank=True, validators=[validate_file_extension])
    fichier_telecharge = models.BooleanField(default=False)

    def __str__(self):
        return self.etat