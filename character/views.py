from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Max    
from .models import Character
from .serializers import CharacterSerializer
from .services import fetch_and_save_characters
from rest_framework.pagination import PageNumberPagination
from .models import Location, Episode
from .serializers import LocationSerializer, EpisodeSerializer

"""
    @AUTHOR: Ivan Sanchez
    @LAST_UPDATE: 2026-09-19
    @DESCRIPTION: Vistas para los endpoints del CRUD de Character y sincronización
"""
@api_view(['GET'])
#* Vista para obtener la lista de personajes paginada y filtrada (Solo activos)
def get_characters(request):
    characters = Character.objects.filter(is_active=True)
    name = request.query_params.get('name', None)
    species = request.query_params.get('species', None)
    status_param = request.query_params.get('status', None)
    gender = request.query_params.get('gender', None)
    if name:
        characters = characters.filter(name__icontains=name)
    if species:
        characters = characters.filter(species__iexact=species)
    if status_param:
        characters = characters.filter(status__iexact=status_param)
    if gender:
        characters = characters.filter(gender__iexact=gender)
    characters = characters.prefetch_related('origin', 'location', 'episodes').order_by('character_id')
    paginator = PageNumberPagination()
    page_obj = paginator.paginate_queryset(characters, request)
    if page_obj is not None:
        serializer = CharacterSerializer(page_obj, many=True)
        return paginator.get_paginated_response(serializer.data)
    serializer = CharacterSerializer(characters, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
#* Vista para obtener los detalles de un personaje específico por ID
def get_character_detail(request, pk):
    character = get_object_or_404(Character, pk=pk, is_active=True)
    serializer = CharacterSerializer(character)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
#* Vista para crear un nuevo personaje personalizado localmente
def create_character(request):
    serializer = CharacterSerializer(data=request.data)
    if serializer.is_valid():
        STARTING_CUSTOM_ID = 1000000
        max_id = Character.objects.aggregate(Max('character_id'))['character_id__max']
        if max_id and max_id >= STARTING_CUSTOM_ID:
            new_character_id = max_id + 1
        else:
            new_character_id = STARTING_CUSTOM_ID
        original_name = serializer.validated_data.get('name', '')
        if not original_name.endswith('(Local)'):
            formatted_name = f"{original_name} (Local)"
        else:
            formatted_name = original_name
        character = serializer.save(
            name=formatted_name,
            character_id=new_character_id,
            is_custom=True,
            is_active=True
        )
        return Response(CharacterSerializer(character).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'PATCH'])
#* Vista para actualizar un personaje específico
def update_character(request, pk):
    character = get_object_or_404(Character, pk=pk, is_active=True)
    serializer = CharacterSerializer(character, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save(is_custom=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
#* Vista para desactivar un personaje específico (Soft Delete)
def delete_character(request, pk):
    character = get_object_or_404(Character, pk=pk)
    character.is_active = False
    character.save()
    return Response({'message': 'Personaje desactivado correctamente.'}, status=status.HTTP_200_OK)

@api_view(['POST'])
#* Vista para activar la sincronización manual desde el Frontend
def sync_characters(request):
    try:
        sync_result = fetch_and_save_characters(target_count=200)
        return Response({
            'message': 'Sincronización manual realizada con éxito.',
            'processed_characters': sync_result['processed_characters'],
            'new_characters_added': sync_result['new_characters_added']
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'error': f'Ocurrió un error al sincronizar con la API externa: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@api_view(['POST'])
#* Vista para reactivar/desborrar un personaje específico
def restore_character(request, pk):
    character = get_object_or_404(Character, pk=pk)
    if character.is_active:
        return Response({'message': 'El personaje ya se encuentra activo.'}, status=status.HTTP_400_BAD_REQUEST)
    character.is_active = True
    character.save()
    serializer = CharacterSerializer(character)
    return Response({
        'message': 'Personaje reactivado correctamente.',
        'data': serializer.data
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
#* Vista para obtener la lista de todas las ubicaciones en BD
def get_locations(request):
    locations = Location.objects.all().order_by('location_id')
    serializer = LocationSerializer(locations, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
#* Vista para obtener la lista de todos los episodios en BD
def get_episodes(request):
    episodes = Episode.objects.all().order_by('episode_id')
    serializer = EpisodeSerializer(episodes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)