# Generated by Django 4.2.2 on 2023-06-11 11:39

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import gestion_ville.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Citoyen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=255)),
                ('adresse', models.CharField(max_length=255)),
                ('telephone', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Signalement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('date_signalement', models.DateTimeField(default=django.utils.timezone.now)),
                ('etat_signalement', models.CharField()),
                ('lieu', models.CharField()),
                ('type_signalement', models.CharField(choices=[('type1', 'Type 1'), ('type2', 'Type 2'), ('type3', 'Type 3')], max_length=20)),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('citoyen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='signalements', to='gestion_ville.citoyen')),
            ],
        ),
        migrations.CreateModel(
            name='Employe',
            fields=[
                ('citoyen_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='gestion_ville.citoyen')),
                ('poste', models.CharField(max_length=255)),
                ('date_naisse', models.DateField()),
                ('salaire', models.PositiveIntegerField()),
            ],
            bases=('gestion_ville.citoyen',),
        ),
        migrations.CreateModel(
            name='Demande',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.TextField()),
                ('date', models.DateField(blank=True)),
                ('etat', models.CharField(blank=True)),
                ('cout', models.PositiveIntegerField(blank=True)),
                ('delai_traitement', models.CharField(blank=True)),
                ('confirm', models.CharField(blank=True)),
                ('fichier', models.FileField(upload_to='demande_files/', validators=[gestion_ville.models.validate_file_extension])),
                ('citoyen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='demandes', to='gestion_ville.citoyen')),
            ],
        ),
        migrations.CreateModel(
            name='Travail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('date_debut', models.DateField()),
                ('date_fin_prevue', models.DateField()),
                ('etat_davancement', models.PositiveIntegerField()),
                ('signalements', models.ManyToManyField(related_name='travaux', to='gestion_ville.signalement')),
                ('employes', models.ManyToManyField(related_name='travaux', to='gestion_ville.employe')),
            ],
        ),
    ]