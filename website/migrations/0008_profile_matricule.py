# Generated by Django 3.0.6 on 2021-01-12 01:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0007_auto_20210112_0139'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='matricule',
            field=models.CharField(blank=True, max_length=250, verbose_name='Matricule'),
        ),
    ]
