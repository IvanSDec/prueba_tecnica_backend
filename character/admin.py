from django.contrib import admin
from .models import Character, Location, Episode

""" 
    @AUTHOR: Ivan Sanchez
    @LAST_UPDATE: 2026-09-19
    @DESCRIPTION: Configuración del panel de administración para los modelos Character, Location y Episode.
"""
@admin.register(Character)
#* Configuración del panel de administración para el modelo Character.
class CharacterAdmin(admin.ModelAdmin):
    list_display = ('id', 'character_id', 'name', 'status', 'species', 'is_custom')
    list_filter = ('status', 'species', 'is_custom')
    search_fields = ('name', 'species')

@admin.register(Location)
#* Configuración del panel de administración para el modelo Location.
class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'location_id', 'name', 'type', 'dimension')
    search_fields = ('name', 'type', 'dimension')

@admin.register(Episode)
#* Configuración del panel de administración para el modelo Episode.
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'episode_id', 'episode', 'name', 'air_date')
    search_fields = ('name', 'episode')