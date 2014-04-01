from django.contrib import admin

from .models import (
    Project, ProjectManager, Team, ProjectProviderSettings,
    UserOAuthToken)


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


class ProjectProviderSettingsAdmin(admin.ModelAdmin):
    pass

admin.site.register(ProjectProviderSettings, ProjectProviderSettingsAdmin)


class UserOAuthTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'identifier', 'token')

admin.site.register(UserOAuthToken, UserOAuthTokenAdmin)
