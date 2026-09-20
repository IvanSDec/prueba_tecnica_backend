from django.urls import path
from .views import (
    user_list,
    user_create,
    user_retrieve,
    user_update,
    user_delete,
    restore_user, 
    CustomTokenObtainPairView
)

"""
    @AUTHOR: Ivan Sanchez
    @LAST_UPDATE: 2026-09-19
    @DESCRIPTION: URLs para los endpoints del CRUD de Usuarios y obtención de Token.
"""
urlpatterns = [
    #* Autenticación
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    #* Rutas separadas del CRUD de Usuarios
    path('list/', user_list, name='user-list'),
    
    #* Rutas individuales del CRUD de Usuarios
    path('create/', user_create, name='user-create'),
    
    #* Rutas individuales del CRUD de Usuarios por ID
    path('<int:pk>/detail/', user_retrieve, name='user-retrieve'),
    
    #* Actualización, eliminación y restauración de usuarios por ID
    path('<int:pk>/update/', user_update, name='user-update'),
    
    #* Actualización de usuarios por ID
    path('<int:pk>/delete/', user_delete, name='user-delete'),
    
    #* Eliminación de usuarios por ID
    path('<int:pk>/restore/', restore_user, name='user-restore'),

]