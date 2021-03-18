from django.contrib import admin
from .models import URLS, Playlists, PlaylistURLS
# Register your models here.

admin.site.register(URLS)
admin.site.register(Playlists)
admin.site.register(PlaylistURLS)
