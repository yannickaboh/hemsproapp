from django.contrib.auth.models import User, Group
import django_filters
from django import forms
from .models import *


# Create your filters here !!!

class GroupFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Group
        fields = ['name',  ]


class PosteFilter(django_filters.FilterSet):
    libelle = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Poste
        fields = ['libelle',   ]


class SiteFilter(django_filters.FilterSet):
    libelle = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Site
        fields = ['libelle',   ]


class CompagnieFilter(django_filters.FilterSet):
    libelle = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Compagnie
        fields = ['libelle',   ]


class ProfileFilter(django_filters.FilterSet):
    matricule = django_filters.CharFilter(field_name='matricule', lookup_expr='iexact')
    poste_libelle = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Profile
        fields = ['poste', 'matricule',   ]