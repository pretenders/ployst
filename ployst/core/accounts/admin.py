from django.contrib import admin

from .models import Project, ProjectManager, Team


class TeamUserInline(admin.TabularInline):
    model = Team.users.through


class TeamAdmin(admin.ModelAdmin):
    inlines = (TeamUserInline,)

admin.site.register(Team, TeamAdmin)


class ProjectManagerInline(admin.TabularInline):
    model = ProjectManager


class ProjectAdmin(admin.ModelAdmin):
    inlines = (ProjectManagerInline,)

admin.site.register(Project, ProjectAdmin)
