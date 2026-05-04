from django.contrib import admin
from .models import Project, ProjectCategory, ProjectRating, ProjectReview, Favorite


class ProjectInline(admin.TabularInline):
    model = Project


class ProjectRatingInline(admin.TabularInline):
    model = ProjectRating


class ProjectReviewInline(admin.TabularInline):
    model = ProjectReview


class FavoriteInline(admin.TabularInline):
    model = Favorite


class ProjectAdmin(admin.ModelAdmin):
    model = Project
    list_display = ['title', 'category','creator', 
                    'description', 'materials', 'steps', 
                    'created_on', 'updated_on']
    inlines = [ProjectRatingInline, ProjectReviewInline, FavoriteInline,]


class ProjectCategoryAdmin(admin.ModelAdmin):
    model = ProjectCategory
    inlines = [ProjectInline,]


admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectCategory, ProjectCategoryAdmin)
