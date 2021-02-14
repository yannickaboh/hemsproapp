# Generated by Django 3.0.6 on 2021-01-03 01:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('website', '0003_auto_20210102_1646'),
    ]

    operations = [
        migrations.CreateModel(
            name='Compagnie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libelle', models.CharField(blank=True, max_length=250, null=True, verbose_name='Libellé')),
                ('abbreviation', models.CharField(blank=True, max_length=250, null=True, verbose_name='Abbréviation')),
                ('telephone', models.CharField(blank=True, max_length=250, null=True, verbose_name='Téléphone')),
                ('fax', models.CharField(blank=True, max_length=250, null=True, verbose_name='Fax')),
                ('email', models.EmailField(blank=True, max_length=250, null=True, verbose_name='Email')),
                ('siteweb', models.CharField(blank=True, max_length=250, null=True, verbose_name='Site Web')),
                ('adresse', models.CharField(blank=True, max_length=250, null=True, verbose_name='Adresse')),
                ('visibilite', models.IntegerField(default=1, verbose_name='Visibilité')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Date de Création')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Date de Modification')),
                ('desactivated', models.DateTimeField(auto_now=True, verbose_name='Date de Désactivation')),
                ('added_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='compagnie_added_by', to=settings.AUTH_USER_MODEL)),
                ('desactivated_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='compagnie_desactivated_by', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='compagnie_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Compagnie',
                'verbose_name_plural': 'Compagnies',
                'db_table': 'Compagnie',
                'ordering': ('created',),
            },
        ),
    ]