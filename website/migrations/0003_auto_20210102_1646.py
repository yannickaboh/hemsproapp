# Generated by Django 3.0.6 on 2021-01-02 15:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('website', '0002_poste'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='poste',
            options={'ordering': ('created',), 'verbose_name': 'Poste', 'verbose_name_plural': 'Postes'},
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libelle', models.CharField(blank=True, max_length=250, null=True, verbose_name='Libellé')),
                ('activite', models.CharField(blank=True, max_length=250, null=True, verbose_name='Activité Principale')),
                ('objectif', models.TextField(blank=True, null=True, verbose_name='Objectifs')),
                ('visibilite', models.IntegerField(default=1, verbose_name='Visibilité')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Date de Création')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Date de Modification')),
                ('desactivated', models.DateTimeField(auto_now=True, verbose_name='Date de Désactivation')),
                ('added_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='site_added_by', to=settings.AUTH_USER_MODEL)),
                ('desactivated_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='site_desactivated_by', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='site_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Site',
                'verbose_name_plural': 'Sites',
                'db_table': 'Site',
                'ordering': ('created',),
            },
        ),
    ]
