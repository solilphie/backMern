from django.contrib import admin
from . import models


@admin.register(models.Post)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('title', 'id' , 'company', 'category','status', 'slug', 'author')
    prepopulated_fields = {'slug': ('title',), }



