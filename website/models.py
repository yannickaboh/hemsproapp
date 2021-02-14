from django.db import models
from django.contrib.auth.models import Group, User 
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime
from datetime import timedelta
from datetime import datetime
from datetime import *
from django.utils import timezone

# Create your models here.

class Mouchard(models.Model):
	action = models.CharField(max_length=250, null=True, blank=True, verbose_name='Action effectuée dans le système')
	created = models.DateTimeField(auto_now_add=True, verbose_name='Date de Création')
	visibilite = models.IntegerField(verbose_name='Visibilité', default=1)

	class Meta:
		db_table = 'Mouchard'
		ordering = ('-created',)
		verbose_name = 'Mouchard'
		verbose_name_plural = 'Mouchards'

	def __str__(self):
		return self.action


class Poste(models.Model):
	libelle = models.CharField(max_length=250, null=True, blank=True, verbose_name='Libellé')
	description = models.TextField(null=True, blank=True, verbose_name='Description')
	visibilite = models.IntegerField(verbose_name='Visibilité', default=1)
	created = models.DateTimeField(auto_now_add=True, verbose_name='Date de Création')
	updated = models.DateTimeField(auto_now=True, verbose_name='Date de Modification')
	desactivated = models.DateTimeField(auto_now=True, verbose_name='Date de Désactivation')
	added_by = models.ForeignKey(User, null=True, blank=True, editable=False, on_delete=models.CASCADE, related_name='%(class)s_added_by')
	updated_by = models.ForeignKey(User, null=True, blank=True, editable=False, on_delete=models.CASCADE, related_name='%(class)s_updated_by')
	desactivated_by = models.ForeignKey(User, null=True, blank=True, editable=False, on_delete=models.CASCADE, related_name='%(class)s_desactivated_by')

	class Meta:
		db_table = 'Poste'
		ordering = ('created',)
		verbose_name = 'Poste'
		verbose_name_plural = 'Postes'

	def __str__(self):
		return self.libelle


class Site(models.Model):
	libelle = models.CharField(max_length=250, null=True, blank=True, verbose_name='Libellé')
	activite = models.CharField(max_length=250, null=True, blank=True, verbose_name='Activité Principale')
	objectif = models.TextField(null=True, blank=True, verbose_name='Objectifs')
	visibilite = models.IntegerField(verbose_name='Visibilité', default=1)
	created = models.DateTimeField(auto_now_add=True, verbose_name='Date de Création')
	updated = models.DateTimeField(auto_now=True, verbose_name='Date de Modification')
	desactivated = models.DateTimeField(auto_now=True, verbose_name='Date de Désactivation')
	added_by = models.ForeignKey(User, null=True, blank=True, editable=False, on_delete=models.CASCADE, related_name='%(class)s_added_by')
	updated_by = models.ForeignKey(User, null=True, blank=True, editable=False, on_delete=models.CASCADE, related_name='%(class)s_updated_by')
	desactivated_by = models.ForeignKey(User, null=True, blank=True, editable=False, on_delete=models.CASCADE, related_name='%(class)s_desactivated_by')

	class Meta:
		db_table = 'Site'
		ordering = ('created',)
		verbose_name = 'Site'
		verbose_name_plural = 'Sites'

	def __str__(self):
		return self.libelle


class Compagnie(models.Model):
	libelle = models.CharField(max_length=250, null=True, blank=True, verbose_name='Libellé')
	abbreviation = models.CharField(max_length=250, null=True, blank=True, verbose_name='Abbréviation')
	telephone = models.CharField(max_length=250, null=True, blank=True, verbose_name='Téléphone')
	fax = models.CharField(max_length=250, null=True, blank=True, verbose_name='Fax')
	email = models.EmailField(max_length=250, null=True, blank=True, verbose_name='Email')
	siteweb = models.CharField(max_length=250, null=True, blank=True, verbose_name='Site Web')
	adresse = models.CharField(max_length=250, null=True, blank=True, verbose_name='Adresse')
	visibilite = models.IntegerField(verbose_name='Visibilité', default=1)
	created = models.DateTimeField(auto_now_add=True, verbose_name='Date de Création')
	updated = models.DateTimeField(auto_now=True, verbose_name='Date de Modification')
	desactivated = models.DateTimeField(auto_now=True, verbose_name='Date de Désactivation')
	added_by = models.ForeignKey(User, null=True, blank=True, editable=False, on_delete=models.CASCADE, related_name='%(class)s_added_by')
	updated_by = models.ForeignKey(User, null=True, blank=True, editable=False, on_delete=models.CASCADE, related_name='%(class)s_updated_by')
	desactivated_by = models.ForeignKey(User, null=True, blank=True, editable=False, on_delete=models.CASCADE, related_name='%(class)s_desactivated_by')

	class Meta:
		db_table = 'Compagnie'
		ordering = ('created',)
		verbose_name = 'Compagnie'
		verbose_name_plural = 'Compagnies'

	def __str__(self):
		return self.libelle

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Profile(models.Model):

	ONLINE = 'En ligne'
	OFFLINE = 'Hors ligne'

	CONNECTED = [
        (ONLINE, 'En ligne'),
        (OFFLINE, 'Hors ligne'),
    ]


	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
	avatar = models.ImageField(upload_to='avatars', blank=True, default='avatars/avatar.jpg', verbose_name='Avatar')
	adresse = models.CharField(max_length=250, blank=True, verbose_name='Adresse')
	telephone = models.CharField(max_length=250, blank=True, verbose_name='Téléphone')
	nationalite = models.CharField(max_length=250, blank=True, verbose_name='Nationalité')
	quartier = models.CharField(max_length=250, blank=True, verbose_name='Quartier')
	matricule = models.CharField(max_length=250, blank=True, verbose_name='Matricule')
	ville = models.CharField(max_length=250, blank=True, verbose_name='Ville')
	poste = models.ForeignKey(Poste, on_delete=models.CASCADE, verbose_name='Poste', blank=True, null=True)
	site = models.ForeignKey(Site, on_delete=models.CASCADE, verbose_name='Site', blank=True, null=True)
	compagnie = models.ForeignKey(Compagnie, on_delete=models.CASCADE, verbose_name='Compagnie', blank=True, null=True)
	groupe = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='Droits d\'accès', blank=True, null=True)
	code = models.CharField(max_length=250, verbose_name='code de Réinitialisation', blank=True)
	connecte = models.CharField(max_length=250, choices=CONNECTED, default=OFFLINE, verbose_name='En ligne ?')
	statut = models.CharField(max_length=250, blank=True, verbose_name='Statut de l\'employé')


	visibilite = models.IntegerField(verbose_name='Visibilité', default=1)
	created = models.DateTimeField(auto_now_add=True, verbose_name='Date de Création')
	updated = models.DateTimeField(auto_now=True, verbose_name='Date de Modification')
	desactivated = models.DateTimeField(auto_now=True, verbose_name='Date de Désactivation')
	added_by = models.ForeignKey(User, null=True, blank=True, editable=False, on_delete=models.CASCADE, related_name='%(class)s_added_by')
	updated_by = models.ForeignKey(User, null=True, blank=True, editable=False, on_delete=models.CASCADE, related_name='%(class)s_updated_by')
	desactivated_by = models.ForeignKey(User, null=True, blank=True, editable=False, on_delete=models.CASCADE, related_name='%(class)s_desactivated_by')

	class Meta:
		db_table = 'Profile'
		ordering = ('created',)
		verbose_name = 'Profile'
		verbose_name_plural = 'Profiles'

	def __str__(self):
		return self.user.username



class Presence(models.Model):

	site = models.ForeignKey(Site, on_delete=models.CASCADE, verbose_name='Site Affilié')
	employe = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Employé Concerné')
	heureArrivee= models.DateTimeField(max_length=250,  verbose_name='Heure d\'arrivée')
	heureDepart = models.DateTimeField(blank=True, null=True, verbose_name='Heure de Départ')
	debutPause = models.DateTimeField(blank=True, null=True, verbose_name='Début de la Pause')
	finPause = models.DateTimeField(blank=True, null=True, verbose_name='Fin de la Pause')
	finPause = models.DateTimeField(blank=True, null=True, verbose_name='Fin de la Pause')

	visibilite = models.IntegerField(verbose_name='Visibilité', default=1)
	created = models.DateTimeField(auto_now_add=True, verbose_name='Date de Création')
	updated = models.DateTimeField(auto_now=True, verbose_name='Date de Modification')
	desactivated = models.DateTimeField(auto_now=True, verbose_name='Date de Désactivation')
	added_by = models.ForeignKey(User, null=True, blank=True, editable=False, on_delete=models.CASCADE, related_name='%(class)s_added_by')
	updated_by = models.ForeignKey(User, null=True, blank=True, editable=False, on_delete=models.CASCADE, related_name='%(class)s_updated_by')
	desactivated_by = models.ForeignKey(User, null=True, blank=True, editable=False, on_delete=models.CASCADE, related_name='%(class)s_desactivated_by')

	class Meta:
		db_table = 'Presence'
		ordering = ('-created',)
		verbose_name = 'Presence'
		verbose_name_plural = 'Presences'

	def __str__(self):
		return '{}'.format(self.employe)



class Modele(models.Model):
	libelle = models.CharField(max_length=250, null=True, blank=True, verbose_name='Libellé')
	
	visibilite = models.IntegerField(verbose_name='Visibilité', default=1)
	created = models.DateTimeField(auto_now_add=True, verbose_name='Date de Création')
	updated = models.DateTimeField(auto_now=True, verbose_name='Date de Modification')
	desactivated = models.DateTimeField(auto_now=True, verbose_name='Date de Désactivation')
	added_by = models.ForeignKey(User, null=True, blank=True, editable=False, on_delete=models.CASCADE, related_name='%(class)s_added_by')
	updated_by = models.ForeignKey(User, null=True, blank=True, editable=False, on_delete=models.CASCADE, related_name='%(class)s_updated_by')
	desactivated_by = models.ForeignKey(User, null=True, blank=True, editable=False, on_delete=models.CASCADE, related_name='%(class)s_desactivated_by')

	class Meta:
		db_table = 'Modele'
		ordering = ('created',)
		verbose_name = 'Modele'
		verbose_name_plural = 'Modeles'

	def __str__(self):
		return self.libelle