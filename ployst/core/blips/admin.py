from django.contrib import admin

from .models import Blip, Stream, Tag


class StreamInline(admin.TabularInline):
    model = Blip.streams.through


class BlipAdmin(admin.ModelAdmin):
    inlines = (StreamInline,)

admin.site.register(Blip, BlipAdmin)
admin.site.register(Stream)
admin.site.register(Tag)
