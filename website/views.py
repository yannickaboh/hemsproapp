from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import Group, User 
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseNotFound
from django.template.loader import render_to_string
from django.views.generic import View

# For pagination
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
 
#importing get_template from loader
from django.template.loader import get_template
 
#import render_to_pdf from util.py 
from .utils import render_to_pdf, get_ip

# For printing
#from weasyprint import HTML
from fpdf import FPDF, HTMLMixin

# For import
from tablib import Dataset

# Import resources
from .resources import *

# Import filter
from .filters import *

# Import from website
from website.models import *

# For manage time
from time import gmtime, strftime, time
from datetime import datetime

# Get operating system
import os

# formats allowed
IMAGE_FILE_TYPES = ['png', 'jpg', 'svg', 'jpeg', 'PNG', 'JPG', 'SVG']

# Create your views here.

# Add decorator to access to this page !!!
@login_required(login_url='/')
def displayMouchard(request):

	# Get all groups
	allMouchards = Mouchard.objects.all()

	# Display template
	return render(request, 'website/displayMouchard.html', {'allMouchards': allMouchards})



# Add decorator to access to this page !!!
@login_required(login_url='/')
def test(request):
	return render(request, 'website/test.html', {})


# Se Connecter
def loginView(request):

	if request.method == 'POST':

		# Get data posted
		post_email = request.POST['email']
		post_password = request.POST['password']

		print(post_email, post_password)

		try:
			# Get user who has this email
			this_user = User.objects.get(email=post_email)

			# Get username
			username = this_user.username
			password = post_password

			# Try to authenticate
			user = authenticate(request, username=username, password=password)
			if user is not None:

				# Try to login
				login(request, user)

				# Get date now()
				horaire = strftime("%A, %d %B %Y à %H:%M:%S", gmtime())

				# Get IP address
				local_ip = get_ip()

				# Mouchard
				mouchard = Mouchard.objects.create(
					action = "L'utilisateur {} s'est connecté le {} avec l'adresse IP suivante : {}".format(request.user.username, horaire, local_ip)
				)

				# Save action
				mouchard.save()

				# Pass messages
				messages.success(request, 'Bienvenue sur HEMSPRO APP !!!')  # <-
				return redirect('test')

			else:

				# Pass messages
				messages.warning(request, 'Les identifiants semblent incorrects, veuillez réesayer svp !!!')  # <-
				return redirect('loginView')

		except ObjectDoesNotExist:

			# Pass messages
			messages.warning(request, 'Cet email n\'est pas dans notre base de données !!!')  # <-
			return redirect('loginView')

		
	
	return render(request, 'website/loginView.html', {})


# Deconnexion du Site
# Add decorator to access to this page !!!
@login_required(login_url='/')
def logoutView(request):

	# Get date now()
	horaire = strftime("%A, %d %B %Y à %H:%M:%S", gmtime())

	# Get IP address
	local_ip = get_ip()

	# Mouchard
	mouchard = Mouchard.objects.create(
		action = "L'utilisateur {} s'est déconnecté le {} avec l'adresse IP suivante : {}".format(request.user.username, horaire, local_ip)
	)

	# Save action
	mouchard.save()

	# Try to disconnect
	logout(request)

	# Redirect to a success page.
	messages.success(request, 'Aurevoir et à la prochaine !!!')  # <-
	return redirect('loginView')


# Add decorator to access to this page !!!
@login_required(login_url='/')
def allGroupes(request):

	# Get all groups
	allgroupes = Group.objects.all()

	# Manage Pagination here
	page = request.GET.get('page', 1)
	paginator = Paginator(allgroupes, 5)
	try:
	    groupes = paginator.page(page)
	except PageNotAnInteger:
	    groupes = paginator.page(1)
	except EmptyPage:
	    groupes = paginator.page(paginator.num_pages)

	# Save action in mouchard here
	##############################

	# Get date now()
	horaire = strftime("%A, %d %B %Y à %H:%M:%S", gmtime())

	# Get IP address
	local_ip = get_ip()

	# Mouchard
	mouchard = Mouchard.objects.create(
		action = "L'utilisateur {} a consulté la liste des groupes le {} avec l'adresse IP suivante : {}".format(request.user.username, horaire, local_ip)
	)

	# Save action
	mouchard.save()

	# Return page
	return render(request, 'website/allGroupes.html', {'groupes':groupes})


# Add decorator to access to this page !!!
@login_required(login_url='/')
def allPostes(request):

	# Get all postes
	allpostes = Poste.objects.all().filter(visibilite=1)

	# Manage Pagination here
	page = request.GET.get('page', 1)
	paginator = Paginator(allpostes, 5)
	try:
	    postes = paginator.page(page)
	except PageNotAnInteger:
	    postes = paginator.page(1)
	except EmptyPage:
	    postes = paginator.page(paginator.num_pages)

	# Save action in mouchard here
	##############################

	# Get date now()
	horaire = strftime("%A, %d %B %Y à %H:%M:%S", gmtime())

	# Get IP address
	local_ip = get_ip()

	# Mouchard
	mouchard = Mouchard.objects.create(
		action = "L'utilisateur {} a consulté la liste des postes le {} avec l'adresse IP suivante : {}".format(request.user.username, horaire, local_ip)
	)

	# Save action
	mouchard.save()

	# Return page
	return render(request, 'website/allPostes.html', {'postes':postes})


# Add decorator to access to this page !!!
@login_required(login_url='/')
def allSites(request):

	# Get all sites
	allsites = Site.objects.all().filter(visibilite=1)

	# Count sites
	num_sites = allsites.count()

	# Manage Pagination here
	page = request.GET.get('page', 1)
	paginator = Paginator(allsites, 5)
	try:
	    sites = paginator.page(page)
	except PageNotAnInteger:
	    sites = paginator.page(1)
	except EmptyPage:
	    sites = paginator.page(paginator.num_pages)

	# Save action in mouchard here
	##############################

	# Get date now()
	horaire = strftime("%A, %d %B %Y à %H:%M:%S", gmtime())

	# Get IP address
	local_ip = get_ip()

	# Mouchard
	mouchard = Mouchard.objects.create(
		action = "L'utilisateur {} a consulté la liste des sites le {} avec l'adresse IP suivante : {}".format(request.user.username, horaire, local_ip)
	)

	# Save action
	mouchard.save()

	# Return page
	return render(request, 'website/allSites.html', {'sites':sites, 'num_sites':num_sites})


# Add decorator to access to this page !!!
@login_required(login_url='/')
def allCompagnies(request):

	# Get all compagnies
	allcompagnies = Compagnie.objects.all().filter(visibilite=1)

	# Manage Pagination here
	page = request.GET.get('page', 1)
	paginator = Paginator(allcompagnies, 5)
	try:
	    compagnies = paginator.page(page)
	except PageNotAnInteger:
	    compagnies = paginator.page(1)
	except EmptyPage:
	    compagnies = paginator.page(paginator.num_pages)

	# Save action in mouchard here
	##############################

	# Get date now()
	horaire = strftime("%A, %d %B %Y à %H:%M:%S", gmtime())

	# Get IP address
	local_ip = get_ip()

	# Mouchard
	mouchard = Mouchard.objects.create(
		action = "L'utilisateur {} a consulté la liste des compagnies le {} avec l'adresse IP suivante : {}".format(request.user.username, horaire, local_ip)
	)

	# Save action
	mouchard.save()

	# Return page
	return render(request, 'website/allCompagnies.html', {'compagnies':compagnies})



# Add decorator to access to this page !!!
@login_required(login_url='/')
def allProfiles(request):

	# Get all profiles
	allprofiles = Profile.objects.all().filter(visibilite=1)
	postes = Poste.objects.all().filter(visibilite=1)
	sites = Site.objects.all().filter(visibilite=1)
	compagnies = Compagnie.objects.all().filter(visibilite=1)
	groupes = Group.objects.all()

	# Manage Pagination here
	page = request.GET.get('page', 1)
	paginator = Paginator(allprofiles, 6)
	try:
	    profiles = paginator.page(page)
	except PageNotAnInteger:
	    profiles = paginator.page(1)
	except EmptyPage:
	    profiles = paginator.page(paginator.num_pages)

	# Save action in mouchard here
	##############################

	# Get date now()
	horaire = strftime("%A, %d %B %Y à %H:%M:%S", gmtime())

	# Get IP address
	local_ip = get_ip()

	# Mouchard
	mouchard = Mouchard.objects.create(
		action = "L'utilisateur {} a consulté la liste des profils le {} avec l'adresse IP suivante : {}".format(request.user.username, horaire, local_ip)
	)

	# Save action
	mouchard.save()

	# Return page
	return render(request, 'website/allProfiles.html', {
		'profiles':profiles,
		'postes':postes,
		'sites':sites,
		'compagnies':compagnies,
		'groupes':groupes,
	})


# Add decorator to access to this page !!!
@login_required(login_url='/')
def allPresencesBySite(request):

	# Get all sites
	allsites = Site.objects.all().filter(visibilite=1)

	# Count sites
	num_sites = allsites.count()

	# Manage Pagination here
	page = request.GET.get('page', 1)
	paginator = Paginator(allsites, 5)
	try:
	    sites = paginator.page(page)
	except PageNotAnInteger:
	    sites = paginator.page(1)
	except EmptyPage:
	    sites = paginator.page(paginator.num_pages)

	# Save action in mouchard here
	##############################

	# Get date now()
	horaire = strftime("%A, %d %B %Y à %H:%M:%S", gmtime())

	# Get IP address
	local_ip = get_ip()

	# Mouchard
	mouchard = Mouchard.objects.create(
		action = "L'utilisateur {} a consulté la liste des sites le {} avec l'adresse IP suivante : {}".format(request.user.username, horaire, local_ip)
	)

	# Save action
	mouchard.save()

	# Return page
	return render(request, 'website/allPresencesBySite.html', {'sites':sites, 'num_sites':num_sites})



# Add decorator to access to this page !!!
@login_required(login_url='/')
def allPresences(request, site_id):

	# Get site
	site = get_object_or_404(Site, pk=site_id)

	# Get all presences
	allpresences = Presence.objects.all().filter(site=site).values('created').distinct()

	# Save action in mouchard here
	##############################

	# Return page
	return render(request, 'website/allPresences.html', {
		'site_id':site_id, 
		'site':site,
		'allpresences':allpresences 
	})




# Add decorator to access to this page !!!
@login_required(login_url='/')
def createGroupe(request):

	if request.method == 'POST':

		# Get data posted
		post_name = request.POST['name']

		# Try if you have already registered this group
		try:
			old_group = Group.objects.get(name=post_name)

			# if true redirect to allGroups
			if old_group:

				# Get date now()
				horaire = strftime("%A, %d %B %Y à %H:%M:%S", gmtime())

				# Get IP address
				local_ip = get_ip()

				# Mouchard
				mouchard = Mouchard.objects.create(
					action = "L'utilisateur {} a tenté de créer le groupe {} pourtant déjà existant le {} avec l'adresse IP suivante : {}".format(request.user.username, post_name, horaire, local_ip)
				)

				# Save action
				mouchard.save()

				# pass message
				messages.success(request, 'Ce Groupe a déjà été crée !!!')  # <-
				return redirect('allGroupes')
			else:
				pass

		except ObjectDoesNotExist:
			pass

		# Creer un nouveau groupe
		new_groupe = Group.objects.create(

			name = post_name,

		)

		# Save request
		new_groupe.save()

		# Get date now()
		horaire = strftime("%A, %d %B %Y à %H:%M:%S", gmtime())

		# Get IP address
		local_ip = get_ip()

		# Mouchard
		mouchard = Mouchard.objects.create(
			action = "L'utilisateur {} a crée le groupe {} le {} avec l'adresse IP suivante : {}".format(request.user.username, post_name, horaire, local_ip)
		)

		# Save action
		mouchard.save()

		# pass message
		messages.success(request, 'Groupe ajouté avec succès !!!')  # <-
		return redirect('allGroupes')

	else:
		# pass message
		messages.warning(request, 'Veuiller remplir les champs requis svp !!!')  # <-
		return redirect('allGroupes')


# Add decorator to access to this page !!!
@login_required(login_url='/')
def createPoste(request):

	if request.method == 'POST':

		# Get data posted
		post_libelle = request.POST['libelle']
		post_description = request.POST['description']

		# Try if you have already registered this group
		try:
			old_poste = Poste.objects.get(libelle=post_libelle)

			# if true redirect to allGroups
			if old_poste:

				# Get date now()
				horaire = strftime("%A, %d %B %Y à %H:%M:%S", gmtime())

				# Get IP address
				local_ip = get_ip()

				# Mouchard
				mouchard = Mouchard.objects.create(
					action = "L'utilisateur {} a tenté de créer le poste {} pourtant déjà existant le {} avec l'adresse IP suivante : {}".format(request.user.username, post_libelle, horaire, local_ip)
				)

				# Save action
				mouchard.save()

				# pass message
				messages.success(request, 'Ce Poste a déjà été crée !!!')  # <-
				return redirect('allPostes')
			else:
				pass

		except ObjectDoesNotExist:
			pass

		# Creer un nouveau poste
		new_poste = Poste.objects.create(

			libelle = post_libelle,
			description = post_description,
			added_by = request.user,

		)

		# Save request
		new_poste.save()

		# Get date now()
		horaire = strftime("%A, %d %B %Y à %H:%M:%S", gmtime())

		# Get IP address
		local_ip = get_ip()

		# Mouchard
		mouchard = Mouchard.objects.create(
			action = "L'utilisateur {} a crée le poste {} le {} avec l'adresse IP suivante : {}".format(request.user.username, post_libelle, horaire, local_ip)
		)

		# Save action
		mouchard.save()

		# pass message
		messages.success(request, 'Poste ajouté avec succès !!!')  # <-
		return redirect('allPostes')

	else:
		# pass message
		messages.warning(request, 'Veuiller remplir les champs requis svp !!!')  # <-
		return redirect('allPostes')


# Add decorator to access to this page !!!
@login_required(login_url='/')
def createSite(request):

	if request.method == 'POST':

		# Get data posted
		post_libelle = request.POST['libelle']
		post_activite = request.POST['activite']
		post_objectif = request.POST['objectif']

		# Try if you have already registered this site
		try:
			old_site = Site.objects.get(libelle=post_libelle)

			# if true redirect to allGroups
			if old_site:

				# Get date now()
				horaire = strftime("%A, %d %B %Y à %H:%M:%S", gmtime())

				# Get IP address
				local_ip = get_ip()

				# Mouchard
				mouchard = Mouchard.objects.create(
					action = "L'utilisateur {} a tenté de créer le site {} pourtant déjà existant le {} avec l'adresse IP suivante : {}".format(request.user.username, post_libelle, horaire, local_ip)
				)

				# Save action
				mouchard.save()

				# pass message
				messages.success(request, 'Ce Site a déjà été crée !!!')  # <-
				return redirect('allSites')
			else:
				pass

		except ObjectDoesNotExist:
			pass

		# Creer un nouveau site
		new_site = Site.objects.create(

			libelle = post_libelle,
			activite = post_activite,
			objectif = post_objectif,
			added_by = request.user,

		)

		# Save request
		new_site.save()

		# Get date now()
		horaire = strftime("%A, %d %B %Y à %H:%M:%S", gmtime())

		# Get IP address
		local_ip = get_ip()

		# Mouchard
		mouchard = Mouchard.objects.create(
			action = "L'utilisateur {} a crée le site {} le {} avec l'adresse IP suivante : {}".format(request.user.username, post_libelle, horaire, local_ip)
		)

		# Save action
		mouchard.save()

		# pass message
		messages.success(request, 'Site ajouté avec succès !!!')  # <-
		return redirect('allSites')

	else:
		# pass message
		messages.warning(request, 'Veuiller remplir les champs requis svp !!!')  # <-
		return redirect('allSites')


# Add decorator to access to this page !!!
@login_required(login_url='/')
def createCompagnie(request):

	if request.method == 'POST':

		# Get data posted
		post_libelle = request.POST['libelle']
		post_abbreviation = request.POST['abbreviation']
		post_telephone = request.POST['telephone']
		post_fax = request.POST['fax']
		post_email = request.POST['email']
		post_siteweb = request.POST['siteweb']
		post_adresse = request.POST['adresse']

		# Try if you have already registered this compagnie
		try:
			old_compagnie = Compagnie.objects.get(libelle=post_libelle)

			# if true redirect to allCompagnies
			if old_compagnie:

				# Get date now()
				horaire = strftime("%A, %d %B %Y à %H:%M:%S", gmtime())

				# Get IP address
				local_ip = get_ip()

				# Mouchard
				mouchard = Mouchard.objects.create(
					action = "L'utilisateur {} a tenté de créer la compagnie {} pourtant déjà existant le {} avec l'adresse IP suivante : {}".format(request.user.username, post_libelle, horaire, local_ip)
				)

				# Save action
				mouchard.save()

				# pass message
				messages.success(request, 'Cette compagnie a déjà été crée !!!')  # <-
				return redirect('allCompagnies')
			else:
				pass

		except ObjectDoesNotExist:
			pass

		# Creer un nouveau compagnie
		new_compagnie = Compagnie.objects.create(

			libelle = post_libelle,
			abbreviation = post_abbreviation,
			telephone = post_telephone,
			fax = post_fax,
			email = post_email,
			siteweb = post_siteweb,
			adresse = post_adresse,
			added_by = request.user,

		)

		# Save request
		new_compagnie.save()

		# Get date now()
		horaire = strftime("%A, %d %B %Y à %H:%M:%S", gmtime())

		# Get IP address
		local_ip = get_ip()

		# Mouchard
		mouchard = Mouchard.objects.create(
			action = "L'utilisateur {} a crée la compagnie {} le {} avec l'adresse IP suivante : {}".format(request.user.username, post_libelle, horaire, local_ip)
		)

		# Save action
		mouchard.save()

		# pass message
		messages.success(request, 'Compagnie ajouté avec succès !!!')  # <-
		return redirect('allCompagnies')

	else:
		# pass message
		messages.warning(request, 'Veuiller remplir les champs requis svp !!!')  # <-
		return redirect('allCompagnies')


# Add decorator to access to this page !!!
@login_required(login_url='/')
def createProfil(request):

	if request.method == 'POST':

		# Get data posted
		post_pseudo = request.POST['pseudo']
		post_password = request.POST['password']
		post_noms = request.POST['noms']
		post_prenoms = request.POST['prenoms']
		post_email = request.POST['email']
		post_matricule = request.POST['matricule']
		post_telephone = request.POST['telephone']
		post_adresse = request.POST['adresse']
		post_nationalite = request.POST['nationalite']
		post_quartier = request.POST['quartier']
		post_ville = request.POST['ville']
		post_poste = request.POST['poste']
		post_site = request.POST['site']
		post_compagnie = request.POST['compagnie']
		post_statut = request.POST['statut']
		post_groupe = request.POST['groupe']

		# Try if you have already registered this profile
		try:
			old_user = User.objects.get(username=post_pseudo)

			# if true redirect to allProfils
			if old_user:

				# Get date now()
				horaire = strftime("%A, %d %B %Y à %H:%M:%S", gmtime())

				# Get IP address
				local_ip = get_ip()

				# Mouchard
				mouchard = Mouchard.objects.create(
					action = "L'utilisateur {} a tenté de créer le {} avec l'adresse IP {}, un profil avec les identifiants suivants {} {} pourtant un profil possède déjà le matricule {}".format(request.user.username, horaire, local_ip, post_noms, post_prenoms, post_matricule)
				)

				# Save action
				mouchard.save()

				# pass message
				messages.success(request, 'Ce profil a déjà été crée !!!')  # <-
				return redirect('allProfiles')
			else:
				pass

		except ObjectDoesNotExist:
			pass

		# Try if you have already registered this profile
		try:
			old_user_email = User.objects.get(email=post_email)

			# if true redirect to allProfils
			if old_user_email:

				# Get date now()
				horaire = strftime("%A, %d %B %Y à %H:%M:%S", gmtime())

				# Get IP address
				local_ip = get_ip()

				# Mouchard
				mouchard = Mouchard.objects.create(
					action = "L'utilisateur {} a tenté de créer le {} avec l'adresse IP {}, un profil avec les identifiants suivants {} {} pourtant un profil possède déjà le matricule {}".format(request.user.username, horaire, local_ip, post_noms, post_prenoms, post_matricule)
				)

				# Save action
				mouchard.save()

				# pass message
				messages.success(request, 'Ce profil a déjà été crée !!!')  # <-
				return redirect('allProfiles')
			else:
				pass

		except ObjectDoesNotExist:
			pass

		# Creer un nouveau profil
		new_user = User.objects.create(

			username = post_pseudo,
			first_name = post_noms,
			last_name = post_prenoms,
			email = post_email,
			is_active = True
		)
		# Set password
		new_user.set_password(post_password)

		# Save request
		new_user.save()

		# Get user
		user = new_user.id

		# Get profile with this user object
		new_profile = Profile.objects.get(user=user)


		# Prepare all instances
		poste = Poste.objects.get(libelle=post_poste)
		site = Site.objects.get(libelle=post_site)
		compagnie = Compagnie.objects.get(libelle=post_compagnie)
		groupe = Group.objects.get(name=post_groupe)

		# Update profile elements
		new_profile.telephone = post_telephone
		new_profile.matricule = post_matricule
		new_profile.adresse = post_adresse
		new_profile.nationalite = post_nationalite
		new_profile.quartier = post_quartier
		new_profile.ville = post_ville
		new_profile.poste = poste
		new_profile.site = site
		new_profile.compagnie = compagnie
		new_profile.groupe = groupe
		new_profile.statut = post_statut
		new_profile.visibilite = 1
		new_profile.added_by = request.user

		# Save request
		new_profile.save()

		# Get date now()
		horaire = strftime("%A, %d %B %Y à %H:%M:%S", gmtime())

		# Get IP address
		local_ip = get_ip()

		# Mouchard
		mouchard = Mouchard.objects.create(
			action = "L'utilisateur {} a crée le {} avec l'adresse IP {}, un profil avec les identifiants suivants {} {}".format(request.user.username, horaire, local_ip, post_noms, post_prenoms)
		)

		# Save action
		mouchard.save()

		# pass message
		messages.success(request, 'Profil ajouté avec succès !!!')  # <-
		return redirect('allProfiles')

	else:
		# pass message
		messages.warning(request, 'Veuiller remplir les champs requis svp !!!')  # <-
		return redirect('allProfiles')


# Add decorator to access to this page !!!
@login_required(login_url='/')
def updateGroupe(request, group_id):

	# Get all groups
	allgroupes = Group.objects.all()

	# Manage Pagination here
	page = request.GET.get('page', 1)
	paginator = Paginator(allgroupes, 5)
	try:
	    groupes = paginator.page(page)
	except PageNotAnInteger:
	    groupes = paginator.page(1)
	except EmptyPage:
	    groupes = paginator.page(paginator.num_pages)

	# Get particular groupe
	groupe = Group.objects.get(pk=group_id)

	if request.method == 'POST':

		# Get data posted
		post_id = request.POST['id']
		post_name = request.POST['name']

		# Try if you have already registered this group
		try:
			old_group = Group.objects.get(name=post_name)

			# if true redirect to allGroups
			if old_group:
				# pass message
				messages.success(request, 'Un Groupe avec ce libellé a déjà été crée !!!')  # <-
				return redirect('allGroupes')
			else:
				pass

		except ObjectDoesNotExist:
			pass

		# Manage new groupe
		try:

			# Creer un nouveau groupe
			update_groupe = Group.objects.get(pk=post_id)

			# Get posted value
			update_groupe.name = post_name

			# Save request
			update_groupe.save()

			# pass message
			messages.success(request, 'Groupe modifié avec succès !!!')  # <-
			return redirect('allGroupes')

		except ObjectDoesNotExist:

			# pass message
			messages.success(request, 'Impossible de modifier ce Groupe !!!')  # <-
			return redirect('allGroupes')

		

	else:
		return render(request, 'website/updateGroupe.html', {
			'groupes':groupes,
			'groupe':groupe,
			'group_id':group_id
		})


# Add decorator to access to this page !!!
@login_required(login_url='/')
def updatePoste(request, poste_id):

	# Get all postes
	allpostes = Poste.objects.all().filter(visibilite=1)

	# Manage Pagination here
	page = request.GET.get('page', 1)
	paginator = Paginator(allpostes, 5)
	try:
	    postes = paginator.page(page)
	except PageNotAnInteger:
	    postes = paginator.page(1)
	except EmptyPage:
	    postes = paginator.page(paginator.num_pages)

	# Get particular poste
	poste = Poste.objects.get(pk=poste_id)

	if request.method == 'POST':

		# Get data posted
		post_id = request.POST['id']
		post_libelle = request.POST['libelle']
		post_description = request.POST['description']

		# Try if you have already registered this poste
		try:
			old_poste = Poste.objects.get(libelle=post_libelle)

			# if true redirect to allPostes
			if old_poste:
				# pass message
				messages.success(request, 'Un Poste avec ce libellé a déjà été crée !!!')  # <-
				return redirect('allPostes')
			else:
				pass

		except ObjectDoesNotExist:
			pass

		# Manage new Poste
		try:

			# Creer un nouveau poste
			update_poste = Poste.objects.get(pk=post_id)

			# Get posted value
			update_poste.libelle = post_libelle
			update_poste.description = post_description

			# Save request
			update_poste.save()

			# pass message
			messages.success(request, 'Poste modifié avec succès !!!')  # <-
			return redirect('allPostes')

		except ObjectDoesNotExist:

			# pass message
			messages.success(request, 'Impossible de modifier ce Poste !!!')  # <-
			return redirect('allPostes')

		

	else:
		return render(request, 'website/updatePoste.html', {
			'postes':postes,
			'poste':poste,
			'poste_id':poste_id
		})


# Add decorator to access to this page !!!
@login_required(login_url='/')
def updateSite(request, site_id):

	# Get all sites
	allsites = Site.objects.all().filter(visibilite=1)

	# Manage Pagination here
	page = request.GET.get('page', 1)
	paginator = Paginator(allsites, 5)
	try:
	    sites = paginator.page(page)
	except PageNotAnInteger:
	    sites = paginator.page(1)
	except EmptyPage:
	    sites = paginator.page(paginator.num_pages)

	# Get particular site
	site = Site.objects.get(pk=site_id)

	if request.method == 'POST':

		# Get data posted
		post_id = request.POST['id']
		post_libelle = request.POST['libelle']
		post_activite = request.POST['activite']
		post_objectif = request.POST['objectif']

		# Try if you have already registered this site
		try:
			old_site = Site.objects.get(libelle=post_libelle)

			# if true redirect to allSites
			if old_site:
				# pass message
				pass
				#messages.success(request, 'Un Site avec ce libellé a déjà été crée !!!')  # <-
				#return redirect('allSites')
			else:
				pass

		except ObjectDoesNotExist:
			pass

		# Manage new site
		try:

			# Creer un nouveau site
			update_site = Site.objects.get(pk=site_id)

			# Get posted value
			update_site.libelle = post_libelle
			update_site.activite = post_activite
			update_site.objectif = post_objectif

			# Save request
			update_site.save()

			# pass message
			messages.success(request, 'Site modifié avec succès !!!')  # <-
			return redirect('allSites')

		except ObjectDoesNotExist:

			# pass message
			messages.success(request, 'Impossible de modifier ce site !!!')  # <-
			return redirect('allSites')

		

	else:
		return render(request, 'website/updateSite.html', {
			'sites':sites,
			'site':site,
			'site_id':site_id
		})



# Add decorator to access to this page !!!
@login_required(login_url='/')
def updateCompagnie(request, compagnie_id):

	# Get all compagnies
	allcompagnies = Compagnie.objects.all().filter(visibilite=1)

	# Manage Pagination here
	page = request.GET.get('page', 1)
	paginator = Paginator(allcompagnies, 5)
	try:
	    compagnies = paginator.page(page)
	except PageNotAnInteger:
	    compagnies = paginator.page(1)
	except EmptyPage:
	    compagnies = paginator.page(paginator.num_pages)

	# Get particular compagnie
	compagnie = Compagnie.objects.get(pk=compagnie_id)

	if request.method == 'POST':

		# Get data posted
		post_id = request.POST['id']
		post_libelle = request.POST['libelle']
		post_abbreviation = request.POST['abbreviation']
		post_telephone = request.POST['telephone']
		post_fax = request.POST['fax']
		post_email = request.POST['email']
		post_siteweb = request.POST['siteweb']
		post_adresse = request.POST['adresse']

		# Try if you have already registered this compagnie
		try:
			old_compagnie = Compagnie.objects.get(libelle=post_libelle)

			# if true redirect to allCompagnies
			if old_compagnie:
				# pass message
				#messages.success(request, 'Une Compagnie avec ce libellé a déjà été crée !!!')  # <-
				#return redirect('allCompagnies')
				pass
			else:
				pass

		except ObjectDoesNotExist:
			pass

		# Manage new compagnie
		try:

			# Creer un nouveau compagnie
			update_compagnie = Compagnie.objects.get(pk=compagnie_id)

			# Get posted value
			update_compagnie.libelle = post_libelle
			update_compagnie.abbreviation = post_abbreviation
			update_compagnie.telephone = post_telephone
			update_compagnie.fax = post_fax
			update_compagnie.email = post_email
			update_compagnie.siteweb = post_siteweb
			update_compagnie.adresse = post_adresse

			# Save request
			update_compagnie.save()

			# pass message
			messages.success(request, 'Compagnie modifié avec succès !!!')  # <-
			return redirect('allCompagnies')

		except ObjectDoesNotExist:

			# pass message
			messages.success(request, 'Impossible de modifier cette Compagnie !!!')  # <-
			return redirect('allCompagnies')

		

	else:
		return render(request, 'website/updateCompagnie.html', {
			'compagnies':compagnies,
			'compagnie':compagnie,
			'compagnie_id':compagnie_id
		})



# Add decorator to access to this page !!!
@login_required(login_url='/')
def updateProfil(request, profil_id):

	# Get all profiles
	profile = get_object_or_404(Profile, pk=profil_id)
	allprofiles = Profile.objects.all().filter(visibilite=1)
	postes = Poste.objects.all().filter(visibilite=1)
	sites = Site.objects.all().filter(visibilite=1)
	compagnies = Compagnie.objects.all().filter(visibilite=1)
	groupes = Group.objects.all()

	# Manage Pagination here
	page = request.GET.get('page', 1)
	paginator = Paginator(allprofiles, 6)
	try:
	    profiles = paginator.page(page)
	except PageNotAnInteger:
	    profiles = paginator.page(1)
	except EmptyPage:
	    profiles = paginator.page(paginator.num_pages)

	if request.method == 'POST':

		# Get data posted
		post_pseudo = request.POST['pseudo']
		post_pk = request.POST['pk']
		post_noms = request.POST['noms']
		post_prenoms = request.POST['prenoms']
		post_email = request.POST['email']
		post_matricule = request.POST['matricule']
		post_telephone = request.POST['telephone']
		post_adresse = request.POST['adresse']
		post_nationalite = request.POST['nationalite']
		post_quartier = request.POST['quartier']
		post_ville = request.POST['ville']
		post_poste = request.POST['poste']
		post_site = request.POST['site']
		post_compagnie = request.POST['compagnie']
		post_statut = request.POST['statut']
		post_groupe = request.POST['groupe']

		# Prepare all instances
		poste = Poste.objects.get(libelle=post_poste)
		site = Site.objects.get(libelle=post_site)
		compagnie = Compagnie.objects.get(libelle=post_compagnie)
		groupe = Group.objects.get(name=post_groupe)

		# Check if post pseudo occurs more than 1
		count_pseudos = Profile.objects.filter(user__username=post_pseudo).count()

		# Check if post email occurs more than 1
		count_emails = Profile.objects.filter(user__email=post_email).count()

		# Check username
		try:
			if count_pseudos > 1:
				messages.success(request, 'Un autre profil possède déjà ce pseudo !!!')  # <-
				return redirect('updateProfil', profile.pk )
			else:
				pass
		except ObjectDoesNotExist:
			pass

		# Check email
		try:
			if count_emails > 1:
				messages.success(request, 'Un autre profil possède déjà cet email !!!')  # <-
				return redirect('updateProfil', profile.pk )
			else:
				pass
		except ObjectDoesNotExist:
			pass

		# Get profil to update
		try:
			update_profile = get_object_or_404(Profile, pk=post_pk)

			# Update ddata
			update_profile.matricule = post_matricule
			update_profile.telephone = post_telephone
			update_profile.adresse = post_adresse
			update_profile.nationalite = post_nationalite
			update_profile.quartier = post_quartier
			update_profile.ville = post_ville
			update_profile.poste = poste
			update_profile.compagnie = compagnie
			update_profile.statut = post_statut
			update_profile.groupe = groupe
			update_profile.updated_by = request.user

			try:
				update_user = get_object_or_404(User, pk=profile.user.pk)

				# Update ddata
				update_user.pseudo = post_pseudo
				update_user.email = post_email

				# Save updates
				update_profile.save()
				update_user.save()

				# Redirect 
				messages.success(request, 'Profil modifié avec succès !!!')  # <-
				return redirect('updateProfil', profile.pk )

				
			except ObjectDoesNotExist:
				messages.success(request, 'Une erreur sur le serveur, impossible de mettre ce profile à jour !!!')  # <-
				return redirect('updateProfil', profile.pk )

		except ObjectDoesNotExist:
			messages.success(request, 'Une erreur sur le serveur, impossible de mettre ce profile à jour !!!')  # <-
			return redirect('updateProfil', profile.pk )
		



	return render(request, 'website/updateProfil.html', {

		'profil_id':profil_id,
		'profile':profile,
		'profiles':profiles,
		'postes':postes,
		'sites':sites,
		'compagnies':compagnies,
		'groupes':groupes,

	})


# updatePassword 
# Add decorator to access to this page !!!
@login_required(login_url='/')
def updatePassword(request, profil_id):

	# Get all profiles
	profile = get_object_or_404(Profile, pk=profil_id)
	allprofiles = Profile.objects.all().filter(visibilite=1)
	postes = Poste.objects.all().filter(visibilite=1)
	sites = Site.objects.all().filter(visibilite=1)
	compagnies = Compagnie.objects.all().filter(visibilite=1)
	groupes = Group.objects.all()

	# Manage Pagination here
	page = request.GET.get('page', 1)
	paginator = Paginator(allprofiles, 6)
	try:
	    profiles = paginator.page(page)
	except PageNotAnInteger:
	    profiles = paginator.page(1)
	except EmptyPage:
	    profiles = paginator.page(paginator.num_pages)

	if request.method == 'POST':

		# Get data posted
		post_new_password = request.POST['new_password']
		post_confirm_password = request.POST['confirm_password']

		# Check if passwords are same
		if post_new_password != post_confirm_password:
			messages.warning(request, 'Les mots de passe ne sont identiques !!!')  # <-
			return redirect('updateProfil', profile.pk )
		else:
			pass

		try:
			# Get user's password to update
			update_user = User.objects.get(pk=profile.user.pk)

			# Update password
			update_user.set_password(post_new_password)
			update_user.save()

			messages.success(request, 'Votre mot de passe a été modifié avec succès !!!')  # <-
			return redirect('updateProfil', profile.pk )

		except ObjectDoesNotExist:
			messages.success(request, 'Impossible de modifier ce mot de passe !!!')  # <-
			return redirect('updateProfil', profile.pk )

	return render(request, 'website/updateProfil.html', {

		'profil_id':profil_id,
		'profile':profile,
		'profiles':profiles,
		'postes':postes,
		'sites':sites,
		'compagnies':compagnies,
		'groupes':groupes,

	})



# updateAvatar 
# Add decorator to access to this page !!!
@login_required(login_url='/')
def updateAvatar(request, profil_id):

	# Get all profiles
	profile = get_object_or_404(Profile, pk=profil_id)
	allprofiles = Profile.objects.all().filter(visibilite=1)
	postes = Poste.objects.all().filter(visibilite=1)
	sites = Site.objects.all().filter(visibilite=1)
	compagnies = Compagnie.objects.all().filter(visibilite=1)
	groupes = Group.objects.all()

	# Manage Pagination here
	page = request.GET.get('page', 1)
	paginator = Paginator(allprofiles, 6)
	try:
	    profiles = paginator.page(page)
	except PageNotAnInteger:
	    profiles = paginator.page(1)
	except EmptyPage:
	    profiles = paginator.page(paginator.num_pages)

	if request.method == 'POST':

		# Get data posted
		post_avatar = request.FILES['avatar']



		try:
			# Start updating here
			profile.avatar = post_avatar
			file_type = profile.avatar.url.split('.')[-1]
			file_type = file_type.lower()
			if file_type in IMAGE_FILE_TYPES:

				profile.save()
				messages.success(request, 'Votre avatar a été modifié avec succès !!!')  # <-
				return redirect('updateProfil', profile.pk )

			else:
				messages.warning(request, 'Le format de fichier image doit être PNG, JPG ou JPEG !!!')  # <-
				return redirect('updateProfil', profile.pk )

		except ObjectDoesNotExist:
			messages.success(request, 'Impossible de modifier cet avatar!!!')  # <-
			return redirect('updateProfil', profile.pk )

	return render(request, 'website/updateProfil.html', {

		'profil_id':profil_id,
		'profile':profile,
		'profiles':profiles,
		'postes':postes,
		'sites':sites,
		'compagnies':compagnies,
		'groupes':groupes,

	})



# Add decorator to access to this page !!!
@login_required(login_url='/')
def desactivatePoste(request, poste_id):

	# Get all postes
	allpostes = Poste.objects.all().filter(visibilite=1)

	# Manage Pagination here
	page = request.GET.get('page', 1)
	paginator = Paginator(allpostes, 5)
	try:
	    postes = paginator.page(page)
	except PageNotAnInteger:
	    postes = paginator.page(1)
	except EmptyPage:
	    postes = paginator.page(paginator.num_pages)

	# Manage desactivation
	try:

		# Get particular poste
		poste = Poste.objects.get(pk=poste_id)

		# Creer un nouveau poste
		update_poste = Poste.objects.get(pk=poste_id)

		# Get posted value
		update_poste.visibilite = 0

		# Save request
		update_poste.save()

		# Get date now()
		horaire = strftime("%A, %d %B %Y à %H:%M:%S", gmtime())

		# Get IP address
		local_ip = get_ip()

		# Mouchard
		mouchard = Mouchard.objects.create(
			action = "L'utilisateur {} a désactivé le poste {} le {} avec l'adresse IP suivante : {}".format(request.user.username, poste, horaire, local_ip)
		)

		# Save action
		mouchard.save()

		# pass message
		messages.success(request, 'Poste désactivé avec succès !!!')  # <-
		return redirect('allPostes')

	except:

		# Get date now()
		horaire = strftime("%A, %d %B %Y à %H:%M:%S", gmtime())

		# Get IP address
		local_ip = get_ip()

		# Mouchard
		mouchard = Mouchard.objects.create(
			action = "L'utilisateur {} a tenté de désactiver le poste {} le {} avec l'adresse IP suivante : {}".format(request.user.username, poste, horaire, local_ip)
		)

		# Save action
		mouchard.save()

		# pass message
		messages.success(request, 'Une erreur s\'est produite lors de la désactivation !!!')  # <-
		return render(request, 'website/allPostes.html', {
			'postes':postes, 
			'poste':poste,
			'poste_id':poste_id
		})


# Add decorator to access to this page !!!
@login_required(login_url='/')
def desactivateGroupe(request, group_id):

	# Get all groupes
	allgroupes = Group.objects.all()

	# Manage Pagination here
	page = request.GET.get('page', 1)
	paginator = Paginator(allgroupes, 5)
	try:
	    groupes = paginator.page(page)
	except PageNotAnInteger:
	    groupes = paginator.page(1)
	except EmptyPage:
	    groupes = paginator.page(paginator.num_pages)

	# Manage desactivation
	try:

		# Get particular groupe
		groupe = Group.objects.get(pk=group_id)

		# Creer un nouveau groupe
		update_groupe = Group.objects.get(pk=poste_id)

		# Get posted value
		update_groupe.visibilite = 0

		# Save request
		update_groupe.save()

		# Get date now()
		horaire = strftime("%A, %d %B %Y à %H:%M:%S", gmtime())

		# Get IP address
		local_ip = get_ip()

		# Mouchard
		mouchard = Mouchard.objects.create(
			action = "L'utilisateur {} a désactivé le groupe {} le {} avec l'adresse IP suivante : {}".format(request.user.username, groupe, horaire, local_ip)
		)

		# Save action
		mouchard.save()

		# pass message
		messages.success(request, 'Groupe désactivé avec succès !!!')  # <-
		return redirect('allGroupes')

	except:

		# Get date now()
		horaire = strftime("%A, %d %B %Y à %H:%M:%S", gmtime())

		# Get IP address
		local_ip = get_ip()

		# Mouchard
		mouchard = Mouchard.objects.create(
			action = "L'utilisateur {} a tenté de désactiver le groupe {} le {} avec l'adresse IP suivante : {}".format(request.user.username, groupe, horaire, local_ip)
		)

		# Save action
		mouchard.save()

		# pass message
		messages.success(request, 'Une erreur s\'est produite lors de la désactivation !!!')  # <-
		return render(request, 'website/allGroupes.html', {
			'groupes':groupes, 
			'groupe':groupe,
			'group_id':group_id
		})


# Add decorator to access to this page !!!
@login_required(login_url='/')
def desactivateSite(request, site_id):

	# Get all sites
	allsites = Site.objects.all().filter(visibilite=1)

	# Manage Pagination here
	page = request.GET.get('page', 1)
	paginator = Paginator(allsites, 5)
	try:
	    sites = paginator.page(page)
	except PageNotAnInteger:
	    sites = paginator.page(1)
	except EmptyPage:
	    sites = paginator.page(paginator.num_pages)

	# Manage desactivation
	try:

		# Get particular site
		site = Site.objects.get(pk=site_id)

		# Creer un nouveau site
		update_site = Site.objects.get(pk=site_id)

		# Get posted value
		update_site.visibilite = 0

		# Save request
		update_site.save()

		# Get date now()
		horaire = strftime("%A, %d %B %Y à %H:%M:%S", gmtime())

		# Get IP address
		local_ip = get_ip()

		# Mouchard
		mouchard = Mouchard.objects.create(
			action = "L'utilisateur {} a désactivé le site {} le {} avec l'adresse IP suivante : {}".format(request.user.username, site, horaire, local_ip)
		)

		# Save action
		mouchard.save()

		# pass message
		messages.success(request, 'Site désactivé avec succès !!!')  # <-
		return redirect('allSites')

	except:

		# Get date now()
		horaire = strftime("%A, %d %B %Y à %H:%M:%S", gmtime())

		# Get IP address
		local_ip = get_ip()

		# Mouchard
		mouchard = Mouchard.objects.create(
			action = "L'utilisateur {} a tenté de désactiver le site {} le {} avec l'adresse IP suivante : {}".format(request.user.username, site, horaire, local_ip)
		)

		# Save action
		mouchard.save()

		# pass message
		messages.success(request, 'Une erreur s\'est produite lors de la désactivation !!!')  # <-
		return render(request, 'website/allSites.html', {
			'sites':sites, 
			'site':site,
			'site_id':site_id
		})


# Add decorator to access to this page !!!
@login_required(login_url='/')
def desactivateCompagnie(request, compagnie_id):

	# Get all compagnies
	allcompagnies = Compagnie.objects.all().filter(visibilite=1)

	# Manage Pagination here
	page = request.GET.get('page', 1)
	paginator = Paginator(allcompagnies, 5)
	try:
	    compagnies = paginator.page(page)
	except PageNotAnInteger:
	    compagnies = paginator.page(1)
	except EmptyPage:
	    compagnies = paginator.page(paginator.num_pages)

	# Manage desactivation
	try:

		# Get particular compagnie
		compagnie = Compagnie.objects.get(pk=compagnie_id)

		# Creer un nouveau compagnie
		update_compagnie = Compagnie.objects.get(pk=compagnie_id)

		# Get posted value
		update_compagnie.visibilite = 0

		# Save request
		update_compagnie.save()

		# Get date now()
		horaire = strftime("%A, %d %B %Y à %H:%M:%S", gmtime())

		# Get IP address
		local_ip = get_ip()

		# Mouchard
		mouchard = Mouchard.objects.create(
			action = "L'utilisateur {} a désactivé la compagnie {} le {} avec l'adresse IP suivante : {}".format(request.user.username, compagnie, horaire, local_ip)
		)

		# Save action
		mouchard.save()

		# pass message
		messages.success(request, 'Compagnie désactivé avec succès !!!')  # <-
		return redirect('allSites')

	except:

		# Get date now()
		horaire = strftime("%A, %d %B %Y à %H:%M:%S", gmtime())

		# Get IP address
		local_ip = get_ip()

		# Mouchard
		mouchard = Mouchard.objects.create(
			action = "L'utilisateur {} a tenté de désactiver la compagnie {} le {} avec l'adresse IP suivante : {}".format(request.user.username, compagnie, horaire, local_ip)
		)

		# Save action
		mouchard.save()

		# pass message
		messages.success(request, 'Une erreur s\'est produite lors de la désactivation !!!')  # <-
		return render(request, 'website/allCompagnies.html', {
			'compagnies':compagnies, 
			'compagnie':compagnie,
			'compagnie_id':compagnie_id
		})



# updateAvatar 
# Add decorator to access to this page !!!
@login_required(login_url='/')
def desactivateProfil(request, profil_id):

	# Get all profiles
	profile = get_object_or_404(Profile, pk=profil_id)
	allprofiles = Profile.objects.all().filter(visibilite=1)
	postes = Poste.objects.all().filter(visibilite=1)
	sites = Site.objects.all().filter(visibilite=1)
	compagnies = Compagnie.objects.all().filter(visibilite=1)
	groupes = Group.objects.all()

	# Manage Pagination here
	page = request.GET.get('page', 1)
	paginator = Paginator(allprofiles, 6)
	try:
	    profiles = paginator.page(page)
	except PageNotAnInteger:
	    profiles = paginator.page(1)
	except EmptyPage:
	    profiles = paginator.page(paginator.num_pages)

	# Manage desactivation
	try:

		# Get particular profile
		desactive_profile = Profile.objects.get(pk=profil_id)

		# Get posted value
		desactive_profile.visibilite = 0

		# Save request
		desactive_profile.save()

		# pass message
		messages.success(request, 'Profil désactivé avec succès !!!')  # <-
		return redirect('allProfiles')

	except ObjectDoesNotExist:

		# pass message
		messages.success(request, 'Impossible de désactiver ce profil, veuillez réesayer !!!')  # <-
		return redirect('allProfiles')



# Add decorator to access to this page !!!
@login_required(login_url='/')
def checkGroupe(request, group_id):

	# Get all groups
	allgroupes = Group.objects.all()

	# Manage Pagination here
	page = request.GET.get('page', 1)
	paginator = Paginator(allgroupes, 5)
	try:
	    groupes = paginator.page(page)
	except PageNotAnInteger:
	    groupes = paginator.page(1)
	except EmptyPage:
	    groupes = paginator.page(paginator.num_pages)

	# Get particular groupe
	groupe = Group.objects.get(pk=group_id)

	# return checkPage
	return render(request, 'website/checkGroupe.html', {
		'groupes':groupes,
		'groupe':groupe,
		'group_id':group_id
	})


# Add decorator to access to this page !!!
@login_required(login_url='/')
def checkPoste(request, poste_id):

	# Get all postes
	allpostes = Poste.objects.all().filter(visibilite=1)

	# Manage Pagination here
	page = request.GET.get('page', 1)
	paginator = Paginator(allpostes, 5)
	try:
	    postes = paginator.page(page)
	except PageNotAnInteger:
	    postes = paginator.page(1)
	except EmptyPage:
	    postes = paginator.page(paginator.num_pages)

	# Get particular poste
	poste = Poste.objects.get(pk=poste_id)

	# return checkPage
	return render(request, 'website/checkPoste.html', {
		'postes':postes,
		'poste':poste,
		'poste_id':poste_id
	})



# Add decorator to access to this page !!!
@login_required(login_url='/')
def checkSite(request, site_id):

	# Get all sites
	allsites = Site.objects.all().filter(visibilite=1)

	# Manage Pagination here
	page = request.GET.get('page', 1)
	paginator = Paginator(allsites, 5)
	try:
	    sites = paginator.page(page)
	except PageNotAnInteger:
	    sites = paginator.page(1)
	except EmptyPage:
	    sites = paginator.page(paginator.num_pages)

	# Get particular site
	site = Site.objects.get(pk=site_id)

	# return checkPage
	return render(request, 'website/checkSite.html', {
		'sites':sites,
		'site':site,
		'site_id':site_id
	})


# Add decorator to access to this page !!!
@login_required(login_url='/')
def checkCompagnie(request, compagnie_id):

	# Get all compagnie
	allcompagnies = Compagnie.objects.all().filter(visibilite=1)

	# Manage Pagination here
	page = request.GET.get('page', 1)
	paginator = Paginator(allcompagnies, 5)
	try:
	    compagnies = paginator.page(page)
	except PageNotAnInteger:
	    compagnies = paginator.page(1)
	except EmptyPage:
	    compagnies = paginator.page(paginator.num_pages)

	# Get particular compagnie
	compagnie = Compagnie.objects.get(pk=compagnie_id)

	# return checkPage
	return render(request, 'website/checkCompagnie.html', {
		'compagnies':compagnies,
		'compagnie':compagnie,
		'compagnie_id':compagnie_id
	})



# Add decorator to access to this page !!!
@login_required(login_url='/')
def checkProfil(request, profil_id):

	# Get all profiles
	his_profile = get_object_or_404(Profile, pk=profil_id)
	allprofiles = Profile.objects.all().filter(visibilite=1)
	postes = Poste.objects.all().filter(visibilite=1)
	sites = Site.objects.all().filter(visibilite=1)
	compagnies = Compagnie.objects.all().filter(visibilite=1)
	groupes = Group.objects.all()

	# Manage Pagination here
	page = request.GET.get('page', 1)
	paginator = Paginator(allprofiles, 6)
	try:
	    profiles = paginator.page(page)
	except PageNotAnInteger:
	    profiles = paginator.page(1)
	except EmptyPage:
	    profiles = paginator.page(paginator.num_pages)

	# return checkPage
	return render(request, 'website/checkProfil.html', {
		'profil_id':profil_id,
		'his_profile':his_profile,
		'profiles':profiles,
		'postes':postes,
		'sites':sites,
		'compagnies':compagnies,
		'groupes':groupes
	})




# Add decorator to access to this page !!!
@login_required(login_url='/')
def exportCSV(request):
    group_resource = GroupResource()
    dataset = group_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="groupes.csv"'
    return response


# Add decorator to access to this page !!!
@login_required(login_url='/')
def exportPosteCSV(request):
    poste_resource = PosteResource()
    dataset = poste_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="postes.csv"'
    return response


# Add decorator to access to this page !!!
@login_required(login_url='/')
def exportSiteCSV(request):
    site_resource = SiteResource()
    dataset = site_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sites.csv"'
    return response


# Add decorator to access to this page !!!
@login_required(login_url='/')
def exportCompagnieCSV(request):
    compagnie_resource = CompagnieResource()
    dataset = compagnie_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="compagnies.csv"'
    return response


# Add decorator to access to this page !!!
@login_required(login_url='/')
def exportProfileCSV(request):
    profile_resource = ProfileResource()
    dataset = profile_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="profiles.csv"'
    return response


# Add decorator to access to this page !!!
@login_required(login_url='/')
def exportXLS(request):
    group_resource = GroupResource()
    dataset = group_resource.export()
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="groupes.xls"'
    return response


# Add decorator to access to this page !!!
@login_required(login_url='/')
def exportPosteXLS(request):
    poste_resource = PosteResource()
    dataset = poste_resource.export()
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="postes.xls"'
    return response


# Add decorator to access to this page !!!
@login_required(login_url='/')
def exportSiteXLS(request):
    site_resource = SiteResource()
    dataset = site_resource.export()
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="sites.xls"'
    return response


# Add decorator to access to this page !!!
@login_required(login_url='/')
def exportCompagnieXLS(request):
    compagnie_resource = CompagnieResource()
    dataset = compagnie_resource.export()
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="compagnies.xls"'
    return response


# Add decorator to access to this page !!!
@login_required(login_url='/')
def exportProfileXLS(request):
    profile_resource = ProfileResource()
    dataset = profile_resource.export()
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="profiles.xls"'
    return response



# Add decorator to access to this page !!!
@login_required(login_url='/')
def exportPDF(request):
    groupes = Group.objects.all()

    #return response
    return render(request, 'website/pdf_template.html', {'groupes':groupes})


# Add decorator to access to this page !!!
@login_required(login_url='/')
def exportPostePDF(request):

	# All Postes
    postes = Poste.objects.all()

    #return response
    return render(request, 'website/postes_pdf_template.html', {'postes':postes})


# Add decorator to access to this page !!!
@login_required(login_url='/')
def exportSitePDF(request):

	# All Sites
    sites = Site.objects.all()

    #return response
    return render(request, 'website/sites_pdf_template.html', {'sites':sites})


# Add decorator to access to this page !!!
@login_required(login_url='/')
def exportCompagniePDF(request):

	# All Compagnies
    compagnies = Compagnie.objects.all()

    #return response
    return render(request, 'website/compagnies_pdf_template.html', {'compagnies':compagnies})


# Add decorator to access to this page !!!
@login_required(login_url='/')
def exportProfilePDF(request):

	# All profiles
    profiles = Profile.objects.all()

    #return response
    return render(request, 'website/profiles_pdf_template.html', {'profiles':profiles})



# Add decorator to access to this page !!!
@login_required(login_url='/')
def importDataGroup(request):

	# Get all groups
	groupes = Group.objects.all()

	# Import data here !
	if request.method == 'POST':
	    group_resource = GroupResource()
	    dataset = Dataset()
	    new_groupes = request.FILES['myfile']

	    #imported_data = dataset.load(new_groupes.read())
	    imported_data = dataset.load(new_groupes.read().decode('utf-8'),format='csv')
	    result = group_resource.import_data(dataset, dry_run=True)  # Test the data import


	    if not result.has_errors():
	        group_resource.import_data(dataset, dry_run=False)  # Actually import now

	return render(request, 'website/allGroupes.html', {'groupes':groupes})


# Add decorator to access to this page !!!
@login_required(login_url='/')
def importDataPoste(request):

	# Get all postes
	postes = Poste.objects.all().filter(visibilite=1)

	# Import data here !
	if request.method == 'POST':
	    poste_resource = PosteResource()
	    dataset = Dataset()
	    new_postes = request.FILES['myfile']

	    #imported_data = dataset.load(new_groupes.read())
	    imported_data = dataset.load(new_postes.read().decode('utf-8'),format='csv')
	    result = poste_resource.import_data(dataset, dry_run=True)  # Test the data import

	    if not result.has_errors():
	        poste_resource.import_data(dataset, dry_run=False)  # Actually import now

	return render(request, 'website/allPostes.html', {'postes':postes})


# Add decorator to access to this page !!!
@login_required(login_url='/')
def importDataSite(request):

	# Get all sites
	sites = Site.objects.all().filter(visibilite=1)

	# Import data here !
	if request.method == 'POST':
	    site_resource = SiteResource()
	    dataset = Dataset()
	    new_sites = request.FILES['myfile']

	    #imported_data = dataset.load(new_groupes.read())
	    imported_data = dataset.load(new_sites.read().decode('utf-8'),format='csv')
	    result = site_resource.import_data(dataset, dry_run=True)  # Test the data import

	    if not result.has_errors():
	        site_resource.import_data(dataset, dry_run=False)  # Actually import now

	return render(request, 'website/allSites.html', {'sites':sites}) 


# Add decorator to access to this page !!!
@login_required(login_url='/')
def importDataCompagnie(request):

	# Get all compagnies
	compagnies = Compagnie.objects.all().filter(visibilite=1)

	# Import data here !
	if request.method == 'POST':
	    compagnie_resource = CompagnieResource()
	    dataset = Dataset()
	    new_compagnies = request.FILES['myfile']

	    #imported_data = dataset.load(new_groupes.read())
	    imported_data = dataset.load(new_compagnies.read().decode('utf-8'),format='csv')
	    result = compagnie_resource.import_data(dataset, dry_run=True)  # Test the data import

	    if not result.has_errors():
	        compagnie_resource.import_data(dataset, dry_run=False)  # Actually import now

	return render(request, 'website/allCompagnies.html', {'compagnies':compagnies})


# Add decorator to access to this page !!!
@login_required(login_url='/')
def importDataProfile(request):

	# Get all profiles
	allprofiles = Profile.objects.all().filter(visibilite=1)
	postes = Poste.objects.all().filter(visibilite=1)
	sites = Site.objects.all().filter(visibilite=1)
	compagnies = Compagnie.objects.all().filter(visibilite=1)
	groupes = Group.objects.all()

	# Manage Pagination here
	page = request.GET.get('page', 1)
	paginator = Paginator(allprofiles, 6)
	try:
	    profiles = paginator.page(page)
	except PageNotAnInteger:
	    profiles = paginator.page(1)
	except EmptyPage:
	    profiles = paginator.page(paginator.num_pages)

	# Import data here !
	if request.method == 'POST':
	    profile_resource = ProfileResource()
	    dataset = Dataset()
	    new_profiles = request.FILES['myfile']

	    #imported_data = dataset.load(new_groupes.read())
	    imported_data = dataset.load(new_profiles.read().decode('utf-8'),format='csv')
	    result = profile_resource.import_data(dataset, dry_run=True)  # Test the data import

	    if not result.has_errors():
	        profile_resource.import_data(dataset, dry_run=False)  # Actually import now
	        messages.success(request, 'Données importées avec succès !!!')  # <-
	        return render(request, 'website/allProfiles.html', {
				'profiles':profiles,
				'postes':postes,
				'sites':sites,
				'compagnies':compagnies,
				'groupes':groupes,
			})
	        
	    else:
	    	# pass message
	    	messages.warning(request, 'Impossible d\'importer ces données !!!')  # <-
	    	# Return page
	    	return render(request, 'website/allProfiles.html', {
				'profiles':profiles,
				'postes':postes,
				'sites':sites,
				'compagnies':compagnies,
				'groupes':groupes,
			})

	else:

		# Return page
		return render(request, 'website/allProfiles.html', {
			'profiles':profiles,
			'postes':postes,
			'sites':sites,
			'compagnies':compagnies,
			'groupes':groupes,
		})