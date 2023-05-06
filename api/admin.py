from django.contrib import admin
from .models import User, ApplicantDetails,DetailAdd
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea, CharField
from django import forms
from django.db import models
from .models import User,DetailAddtwo
# Register your models here.
class UserAdminConfig(UserAdmin):
    model = User
    search_fields = ('email', 'user_name',)
    list_filter = ('email', 'user_name', 'is_active', 'is_staff')
    ordering = ('-start_date',)
    list_display = ('email', 'id', 'user_name', 
                    'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'user_name', )}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Personal', {'fields': ('about',)}),
    )
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 20, 'cols': 60})},
    }
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'user_name', 'password1', 'password2', 'is_active', 'is_staff')}
         ),
    )


admin.site.register(User)
admin.site.register(ApplicantDetails)
admin.site.register(DetailAdd)
admin.site.register(DetailAddtwo)