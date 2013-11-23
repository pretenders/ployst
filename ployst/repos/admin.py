from django.contrib import admin

from .models import Branch, Repository


class BranchAdmin(admin.ModelAdmin):
    pass

admin.site.register(Branch, BranchAdmin)


class RepositoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Repository, RepositoryAdmin)
