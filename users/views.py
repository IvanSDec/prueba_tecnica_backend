from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import User
from .serializers import UserSerializer, CustomTokenObtainPairSerializer
from .permissions import CanViewUsers, CanEditUsers
from rest_framework_simplejwt.views import TokenObtainPairView

"""
    @AUTHOR: Ivan Sanchez
    @LAST_UPDATE: 2026-09-19
    @DESCRIPTION: Vistas para el CRUD completo de Usuarios y autenticación con permisos JWT.
"""
#* Vista para listar usuarios.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_list(request):
    if not CanViewUsers().has_permission(request, None):
        return Response({'detail': 'No tienes permisos para ver usuarios.'}, status=status.HTTP_403_FORBIDDEN)

    users = User.objects.filter(is_active=True)
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

#* Vista para crear usuarios.
@api_view(['POST'])
@permission_classes([AllowAny])
def user_create(request):
    if 'password' not in request.data:
        return Response(
            {"password": ["Este campo es requerido."]},
            status=status.HTTP_400_BAD_REQUEST
        )

    serializer = UserSerializer(
        data=request.data,
        context={
            'request': request,
            'registration': not request.user.is_authenticated
        }
    )
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#* Vista para recuperar un usuario específico.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_retrieve(request, pk):
    if not CanViewUsers().has_permission(request, None):
        return Response({'detail': 'No tienes permiso para ver este usuario.'}, status=status.HTTP_403_FORBIDDEN)

    user = get_object_or_404(User, pk=pk)
    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)

#* Vista para actualizar un usuario específico. 
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def user_update(request, pk):
    if not CanEditUsers().has_permission(request, None):
        return Response({'detail': 'No tienes permiso para editar usuarios.'}, status=status.HTTP_403_FORBIDDEN)

    user = get_object_or_404(User, pk=pk)
    serializer = UserSerializer(user, data=request.data, partial=(request.method == 'PATCH'))
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#* Vista para eliminar un usuario específico. 
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def user_delete(request, pk):
    if not CanEditUsers().has_permission(request, None):
        return Response({'detail': 'No tienes permiso para desactivar usuarios.'}, status=status.HTTP_403_FORBIDDEN)

    user = get_object_or_404(User, pk=pk)
    user.is_active = False
    user.save()
    return Response({"message": "Usuario desactivado correctamente (Soft Delete)."}, status=status.HTTP_200_OK)


#* Vista para restaurar un usuario específico.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def restore_user(request, pk):
    if not CanEditUsers().has_permission(request, None):
        return Response({'detail': 'No tienes permiso para restaurar usuarios.'}, status=status.HTTP_403_FORBIDDEN)
        
    user = get_object_or_404(User, pk=pk)
    if user.is_active:
        return Response({'message': 'El usuario ya se encuentra activo.'}, status=status.HTTP_400_BAD_REQUEST)
        
    user.is_active = True
    user.save()
    serializer = UserSerializer(user)
    return Response({
        'message': 'Usuario reactivado correctamente.',
        'data': serializer.data
    }, status=status.HTTP_200_OK)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer