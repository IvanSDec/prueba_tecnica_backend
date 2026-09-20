from django.urls import path
from .views import (
    user_list_create, 
    user_detail, 
    restore_user, 
    CustomTokenObtainPairView
)

"""
AUTHOR: Ivan Sanchez
LAST_UPDATE: 2026-09-19
DESCRIPTION: URLs para los endpoints del CRUD de Usuarios y obtención de Token.
"""
urlpatterns = [
    #* Autenticación
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    #* CRUD de Usuarios
    path('', user_list_create, name='user-list-create'),
    path('<int:pk>/', user_detail, name='user-detail'),
    path('<int:pk>/restore/', restore_user, name='user-restore'),
]