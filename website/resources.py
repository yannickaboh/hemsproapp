from import_export import resources
from import_export.fields import Field
from django.contrib.auth.models import User, Group
from .models import *


# Create your resource here !!


class GroupResource(resources.ModelResource):
    class Meta:
        model = Group
        fields = ('id', 'name', )
        export_order = ('id', 'name')

class PosteResource(resources.ModelResource):
    class Meta:
        model = Poste
        fields = ('id', 'libelle', )
        export_order = ('id', 'libelle')

class SiteResource(resources.ModelResource):
    class Meta:
        model = Site
        fields = ('id', 'libelle', 'activite', 'objectif')
        export_order = ('id', 'libelle')

class CompagnieResource(resources.ModelResource):
    class Meta:
        model = Compagnie
        fields = ('id', 'libelle', 'abbreviation', 'telephone', 'fax', 'email', 'siteweb', 'adresse')
        export_order = ('id', 'libelle')

class ProfileResource(resources.ModelResource):
    
    Num = Field(attribute='user', column_name='Num')
    Noms = Field(attribute='user__first_name', column_name='Noms')
    Prénoms = Field(attribute='user__last_name', column_name='Prénoms')
    Matricule = Field(attribute='matricule', column_name='Matricule')
    Email = Field(attribute='user__email', column_name='Email')
    Téléphone = Field(attribute='telephone', column_name='Téléphone')
    Poste = Field(attribute='poste', column_name='Poste')
    Site = Field(attribute='site', column_name='Site')
    Compagnie = Field(attribute='compagnie', column_name='Compagnie')

    class Meta:
        model = Profile
        export_order = ('Num', 'Noms', 'Prénoms', 'Email', 'Matricule', 'Téléphone', 'Poste', 'Site', 'Compagnie')
        exclude = ('user', 'user__first_name', 'user__last_name', 'user__email', 'telephone', 'poste', 'site', 'compagnie', 
            'matricule', 'avatar', 'quartier', 'ville', 'groupe', 'code', 'connecte', 'created', 'visibilite', 'updated',
             'desactivated', 'added_by', 'updated_by', 'desactivated_by')