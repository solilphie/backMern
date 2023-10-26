from django.contrib import admin

from django.contrib import admin
from . import models


@admin.register(models.Application)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email' , 'resume', 'coverletter', 'jobid', 'author')


admin.site.register(models.Category)
