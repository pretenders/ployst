from django.contrib import admin

from .models import Branch, Repository


class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'head', 'repo')

admin.site.register(Branch, BranchAdmin)


class RepositoryAdmin(admin.ModelAdmin):
    list_display = ('owner', 'name', 'project')
    list_filter = ('project', 'owner')

admin.site.register(Repository, RepositoryAdmin)
