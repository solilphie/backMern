from django.contrib import admin
from users.models import NewUser
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea, CharField
from django import forms
from django.db import models


class UserAdminConfig(UserAdmin):
    model = NewUser
    search_fields = ('email', 'first_name','last_name')
    list_filter = ('email', 'first_name','last_name', 'is_active', 'is_staff')
    ordering = ('-start_date',)
    list_display = ('email','id', 'first_name','last_name','usertypes','categoryy',
                    'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('first_name','last_name','adress','email', 'usertypes','categoryy')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Personal', {'fields': ('about',)}),
    )
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 20, 'cols': 60})},
    }
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name','last_name','adress','email', 'usertypes','categoryy','password1', 'password2', )}
         ),
    )


admin.site.register(NewUser, UserAdminConfig)
