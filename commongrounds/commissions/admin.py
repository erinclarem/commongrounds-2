from django.contrib import admin
from .models import CommissionType, Commission

class CommissionTypeAdmin(admin.ModelAdmin):
    model = Commission
    list_display = ['name']

class CommissionAdmin(admin.ModelAdmin):
    model = Commission
    list_display = ['title', 'people_required', 'created_on']

admin.site.register(CommissionType, CommissionTypeAdmin)
admin.site.register(Commission, CommissionAdmin)
