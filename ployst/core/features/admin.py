from django.contrib import admin

from .models import Feature, Project, ProjectManager


class FeatureAdmin(admin.ModelAdmin):
    pass

admin.site.register(Feature, FeatureAdmin)


class ProjectManagerInline(admin.TabularInline):
    model = ProjectManager


class ProjectAdmin(admin.ModelAdmin):
    inlines = (ProjectManagerInline,)

admin.site.register(Project, ProjectAdmin)
