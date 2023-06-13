# Generated by Django 4.2.1 on 2023-06-11 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_ville', '0004_alter_signalement_type_signalement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signalement',
            name='type_signalement',
            field=models.CharField(choices=[('accident', 'Accident de la circulation'), ('nuisances', 'Nuisances sonores'), ('degradation', 'Dégradation des espaces publics'), ('eclairage', "Pannes d'éclairage public"), ('assainissement', "Problèmes d'assainissement"), ('graffiti', 'Tags et graffiti'), ('dechets', 'Dépôts sauvages de déchets'), ('infrastructures', 'Dommages aux infrastructures publiques'), ('vandalisme', 'Vandalisme'), ('stationnement', 'Problèmes de stationnement')], max_length=20),
        ),
    ]
