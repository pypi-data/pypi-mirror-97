from django.contrib import admin
from djangofile.models import FileModel
from djangofile.modeladmins import FileModelAdmin

# Register your models here.
admin.site.register(FileModel, FileModelAdmin)
