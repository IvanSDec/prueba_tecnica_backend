from django.urls import path
from .views import (
    get_characters, 
    get_character_detail, 
    create_character,
    update_character, 
    delete_character, 
    restore_character,
    sync_characters,
    get_locations,
    get_episodes,
)

"""
AUTHOR: Ivan Sanchez
LAST_UPDATE: 2026-09-19
DESCRIPTION: URLs para los endpoints de Character
"""
urlpatterns = [
    #* Endpoint para listar todos los personajes
    path('', get_characters, name='get-characters'),
    
    #* Endpoint para crear un nuevo personaje local
    path('create/', create_character, name='create-character'),
    
    #* Endpoint para traer un personaje específico por su ID
    path('<int:pk>/', get_character_detail, name='get-character-detail'),
    
    #* Endpoint para actualizar un personaje específico
    path('<int:pk>/update/', update_character, name='update-character'),
    
    #* Endpoint para desactivar (soft delete) un personaje específico
    path('<int:pk>/delete/', delete_character, name='delete-character'),
    
    #* Endpoint para ejecutar la sincronización manual desde el Frontend
    path('sync/', sync_characters, name='sync-characters'),
    
    #* Endpoint para reactivar/desborrar un personaje específico
    path('<int:pk>/restore/', restore_character, name='restore-character'),
    
    #* Endpoint para obtener la lista de todas las ubicaciones en BD
    path('locations/', get_locations, name='get-locations'),
    
    #* Endpoint para obtener la lista de todos los episodios en BD
    path('episodes/', get_episodes, name='get-episodes'),
    
]