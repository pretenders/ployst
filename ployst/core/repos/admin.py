from django.contrib import admin

from .models import Branch, Repository


class BranchAdmin(admin.ModelAdmin):
    pass

admin.site.register(Branch, BranchAdmin)


def create_hooks(modeladmin, request, queryset):
    """
    Create hooks for the repositories.

    TODO: For testing purposes only - this should be removed when we have this
    hooked up to the front end, as we are importing github stuff into core.
    """
    from ployst.github.views.hook import create_hook

    for obj in queryset:
        create_hook(request, obj.owner, obj.name)


class RepositoryAdmin(admin.ModelAdmin):
    actions = [create_hooks]
    list_display = ('owner', 'name', 'project')
    list_filter = ('project', 'owner')

admin.site.register(Repository, RepositoryAdmin)
