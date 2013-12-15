from django.contrib import admin

from .models import Feature, Project


class FeatureAdmin(admin.ModelAdmin):
    pass

admin.site.register(Feature, FeatureAdmin)


class ProjectAdmin(admin.ModelAdmin):
    pass

admin.site.register(Project, ProjectAdmin)
