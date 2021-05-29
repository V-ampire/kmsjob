from django.contrib import admin
from .models import Vacancy


class VacancyAdmin(admin.ModelAdmin):
    
    list_filter = ('source_name', 'modified')

admin.site.register(Vacancy, VacancyAdmin)