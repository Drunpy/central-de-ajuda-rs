from django.contrib import admin
from abrigos.models import *
# Register your models here.
class AbrigosAdmin(admin.ModelAdmin):
    model = Abrigos

admin.site.register(Abrigos, AbrigosAdmin)