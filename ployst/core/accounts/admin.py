from django.contrib import admin

from .models import Team


class TeamUserInline(admin.TabularInline):
    model = Team.users.through


class TeamAdmin(admin.ModelAdmin):
    inlines = (TeamUserInline,)

admin.site.register(Team, TeamAdmin)
