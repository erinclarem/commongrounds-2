from django.contrib import admin
from .models import Project, ProjectCategory


class ProjectInline(admin.TabularInline):
    model = Project


class ProjectAdmin(admin.ModelAdmin):
    model = Project
    list_display = ['title', 'category', 'created_on', 'updated_on']


class ProjectCategoryAdmin(admin.ModelAdmin):
    model = ProjectCategory
    inlines = [ProjectInline,]


admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectCategory, ProjectCategoryAdmin)
