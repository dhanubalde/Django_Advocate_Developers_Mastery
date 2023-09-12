from django.contrib import admin
from . models import Advocate, Company


@admin.register(Advocate)
class AdvocateAdmin(admin.ModelAdmin):
    list_display =  ['username', 'bio']
    list_filter  =  ['username', 'bio']
    
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display =  ['name', 'bio']
    list_filter  =  ['name', 'bio']