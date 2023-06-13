# Generated by Django 4.2.2 on 2023-06-13 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_ville', '0009_demande_fichier_telecharge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='travail',
            name='date_debut',
        ),
        migrations.RemoveField(
            model_name='travail',
            name='date_fin_prevue',
        ),
        migrations.AlterField(
            model_name='signalement',
            name='etat_signalement',
            field=models.CharField(default='en cours', max_length=50),
        ),
        migrations.AlterField(
            model_name='signalement',
            name='lieu',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='signalement',
            name='type_signalement',
            field=models.CharField(choices=[('accident', 'Accident de la circulation'), ('nuisances', 'Nuisances sonores'), ('degradation', 'Dégradation des espaces publics'), ('eclairage', "Pannes d'éclairage public"), ('assainissement', "Problèmes d'assainissement"), ('graffiti', 'Tags et graffiti'), ('dechets', 'Dépôts sauvages de déchets'), ('infrastructures', 'Dommages aux infrastructures publiques'), ('vandalisme', 'Vandalisme'), ('stationnement', 'Problèmes de stationnement')], max_length=20),
        ),
        migrations.AlterField(
            model_name='travail',
            name='etat_davancement',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=5),
        ),
    ]