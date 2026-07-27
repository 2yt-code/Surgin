from django.contrib import admin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from apps.v1.artist.models import Artist

class MyAdmin(TreeAdmin):
    form = movenodeform_factory(Artist)

admin.site.register(Artist, MyAdmin)