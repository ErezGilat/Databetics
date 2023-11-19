from django.contrib import admin
from .models import DIAGNOSE
from import_export.admin import ExportMixin

class DiagnoseAdmin(ExportMixin ,admin.ModelAdmin):
    list_display = ('diagnosed', 'output')
    list_filter = ('diagnosed', 'output')
    list_per_page = 25
    list_max_show_all = 100

admin.site.register(DIAGNOSE, DiagnoseAdmin)
