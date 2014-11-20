from django.contrib import admin

from .models import (
    Project, ProjectProviderSettings,
    UserOAuthToken
)


class ProjectUserInline(admin.TabularInline):
    model = Project.users.through


class ProjectAdmin(admin.ModelAdmin):
    inlines = (ProjectUserInline,)

admin.site.register(Project, ProjectAdmin)


class ProjectProviderSettingsAdmin(admin.ModelAdmin):
    pass

admin.site.register(ProjectProviderSettings, ProjectProviderSettingsAdmin)


class UserOAuthTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'identifier', 'token')

admin.site.register(UserOAuthToken, UserOAuthTokenAdmin)
