"""hemsproapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# import website views
from website import views
from django_filters.views import FilterView
from website.filters import *


urlpatterns = [
    path('admin/', admin.site.urls),


    # Controller du Mouchard
    path('mouchard/', views.displayMouchard, name='displayMouchard'),

    # Controllers de connexion, deconnexion
    path('', views.loginView, name='loginView'), 
    path('deconnexion/', views.logoutView, name='logoutView'),

    # Controllers de Creation
    path('creer-nouveau-groupe/', views.createGroupe, name='createGroupe'),
    path('creer-nouveau-poste/', views.createPoste, name='createPoste'),
    path('creer-nouveau-site/', views.createSite, name='createSite'),
    path('creer-nouveau-compagnie/', views.createCompagnie, name='createCompagnie'),
    path('creer-nouveau-profil/', views.createProfil, name='createProfil'),

    # Controllers de Listing
    path('listing-des-groupes/', views.allGroupes, name='allGroupes'),
    path('listing-des-postes/', views.allPostes, name='allPostes'),
    path('listing-des-sites/', views.allSites, name='allSites'),
    path('listing-des-compagnies/', views.allCompagnies, name='allCompagnies'),
    path('listing-des-profils/', views.allProfiles, name='allProfiles'),
    path('listing-des-fiches-par-site/', views.allPresencesBySite, name='allPresencesBySite'),
    path('listing-des-fiches-de-presence/<int:site_id>/', views.allPresences, name='allPresences'),

    # Controllers de Modification
    path('modifier-groupe/<int:group_id>/', views.updateGroupe, name='updateGroupe'),
    path('modifier-poste/<int:poste_id>/', views.updatePoste, name='updatePoste'),
    path('modifier-site/<int:site_id>/', views.updateSite, name='updateSite'),
    path('modifier-compagnie/<int:compagnie_id>/', views.updateCompagnie, name='updateCompagnie'),
    path('modifier-profil/<int:profil_id>/', views.updateProfil, name='updateProfil'),
    path('modifier-mot-de-passe/<int:profil_id>/', views.updatePassword, name='updatePassword'),
    path('modifier-avatar/<int:profil_id>/', views.updateAvatar, name='updateAvatar'),

    # Controllers de Désactivation
    path('desactiver-un-poste/<int:poste_id>/', views.desactivatePoste, name='desactivatePoste'),
    path('desactiver-un-groupe/<int:group_id>/', views.desactivateGroupe, name='desactivateGroupe'),
    path('desactiver-un-site/<int:site_id>/', views.desactivateSite, name='desactivateSite'),
    path('desactiver-un-compagnie/<int:compagnie_id>/', views.desactivateCompagnie, name='desactivateCompagnie'),
    path('desactiver-un-profil/<int:compagnie_id>/', views.desactivateProfil, name='desactivateProfil'),

    # Controllers de Checking
    path('consulter-detail-groupe/<int:group_id>/', views.checkGroupe, name='checkGroupe'),
    path('consulter-detail-poste/<int:poste_id>/', views.checkPoste, name='checkPoste'),
    path('consulter-detail-site/<int:site_id>/', views.checkSite, name='checkSite'),
    path('consulter-detail-compagnie/<int:compagnie_id>/', views.checkCompagnie, name='checkCompagnie'),
    path('consulter-detail-profil/<int:profil_id>/', views.checkProfil, name='checkProfil'),

    # Controllers de Recherche
    path('rechercher-un-groupe/', FilterView.as_view(filterset_class=GroupFilter,
        template_name='website/searchGroup.html'), name='searchGroup'),
    path('rechercher-un-poste/', FilterView.as_view(filterset_class=PosteFilter,
        template_name='website/searchPoste.html'), name='searchPoste'),
    path('rechercher-un-site/', FilterView.as_view(filterset_class=SiteFilter,
        template_name='website/searchSite.html'), name='searchSite'),
    path('rechercher-un-compagnie/', FilterView.as_view(filterset_class=CompagnieFilter,
        template_name='website/searchCompagnie.html'), name='searchCompagnie'),
    path('rechercher-un-profil/', FilterView.as_view(filterset_class=ProfileFilter,
        template_name='website/searchProfile.html'), name='searchProfile'),

    # Controllers d'exportation en CSV
    path('exporter-groupes-csv/', views.exportCSV, name='exportCSV'),
    path('exporter-postes-csv/', views.exportPosteCSV, name='exportPosteCSV'),
    path('exporter-sites-csv/', views.exportSiteCSV, name='exportSiteCSV'),
    path('exporter-compagnies-csv/', views.exportCompagnieCSV, name='exportCompagnieCSV'),
    path('exporter-profils-csv/', views.exportProfileCSV, name='exportProfileCSV'),

    # Controllers d'exportation en XLS
    path('exporter-groupes-xls/', views.exportXLS, name='exportXLS'),
    path('exporter-postes-xls/', views.exportPosteXLS, name='exportPosteXLS'),
    path('exporter-sites-xls/', views.exportSiteXLS, name='exportSiteXLS'),
    path('exporter-compagnies-xls/', views.exportCompagnieXLS, name='exportCompagnieXLS'),
    path('exporter-profils-xls/', views.exportProfileXLS, name='exportProfileXLS'),

    # Controllers d'exportation en PDF
    path('exporter-groupes-pdf/', views.exportPDF, name='exportPDF'),
    path('exporter-postes-pdf/', views.exportPostePDF, name='exportPostePDF'),
    path('exporter-sites-pdf/', views.exportSitePDF, name='exportSitePDF'),
    path('exporter-compagnies-pdf/', views.exportCompagniePDF, name='exportCompagniePDF'),
    path('exporter-profils-pdf/', views.exportProfilePDF, name='exportProfilePDF'),

    # Controllers d'importation 
    path('importer-groupes/', views.importDataGroup, name='importDataGroup'),
    path('importer-postes/', views.importDataPoste, name='importDataPoste'),
    path('importer-sites/', views.importDataSite, name='importDataSite'),
    path('importer-compagnies/', views.importDataCompagnie, name='importDataCompagnie'),
    path('importer-profils/', views.importDataProfile, name='importDataProfile'),



    path('test/', views.test, name='test'),
]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
