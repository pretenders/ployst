from django.contrib import admin

from .models import Feature


class FeatureAdmin(admin.ModelAdmin):
    pass

admin.site.register(Feature, FeatureAdmin)
