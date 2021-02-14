from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.conf import settings

# Get all models
from .models import *


# Register your models here.


class MouchardAdmin(admin.ModelAdmin):
    list_display = ['action', 'created']
    list_per_page = 10

admin.site.register(Mouchard, MouchardAdmin)


class PosteAdmin(admin.ModelAdmin):
    list_display = ['libelle', 'description', 'created']
    list_per_page = 10

admin.site.register(Poste, PosteAdmin)


class SiteAdmin(admin.ModelAdmin):
    list_display = ['libelle', 'activite', 'objectif', 'created']
    list_per_page = 10

admin.site.register(Site, SiteAdmin)


class CompagnieAdmin(admin.ModelAdmin):
    list_display = ['libelle', 'abbreviation', 'email', 'telephone', 'siteweb', 'created']
    list_per_page = 10

admin.site.register(Compagnie, CompagnieAdmin)



class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)