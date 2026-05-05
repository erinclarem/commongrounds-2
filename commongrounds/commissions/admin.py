from django.contrib import admin
 
from .models import Commission, CommissionType, Job, JobApplication
 
 
class JobInline(admin.TabularInline):
    model = Job
    extra = 1
 
 
class JobApplicationInline(admin.TabularInline):
    model = JobApplication
    extra = 0
 
 
class CommissionTypeAdmin(admin.ModelAdmin):
    model = CommissionType
    search_fields = ('name',)
    list_display = ('name',)
 
 
class CommissionAdmin(admin.ModelAdmin):
    model = Commission
    search_fields = ('title',)
    list_display = ('title', 'maker', 'status', 'created_on')
    list_filter = ('status', 'type')
    inlines = [JobInline]
 
 
class JobAdmin(admin.ModelAdmin):
    model = Job
    list_display = ('role', 'commission', 'manpower_required', 'status')
    list_filter = ('status',)
    inlines = [JobApplicationInline]
 
 
class JobApplicationAdmin(admin.ModelAdmin):
    model = JobApplication
    list_display = ('applicant', 'job', 'status', 'applied_on')
    list_filter = ('status',)
 
 
admin.site.register(CommissionType, CommissionTypeAdmin)
admin.site.register(Commission, CommissionAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(JobApplication, JobApplicationAdmin)
