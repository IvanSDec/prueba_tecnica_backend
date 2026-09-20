# character/serializers.py
from rest_framework import serializers
from .models import Character, Location, Episode

"""
AUTHOR: Ivan Sanchez
LAST_UPDATE: 2026-09-19
DESCRIPTION: Serializers para los modelos de Character, Location y Episode
"""
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'location_id', 'name', 'type', 'dimension', 'url']

class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = ['id', 'episode_id', 'name', 'air_date', 'episode', 'url']

class CharacterSerializer(serializers.ModelSerializer):
    origin_detail = LocationSerializer(source='origin', read_only=True)
    location_detail = LocationSerializer(source='location', read_only=True)
    episodes_detail = EpisodeSerializer(source='episodes', many=True, read_only=True)

    class Meta:
        model = Character
        fields = [
            'id', 
            'character_id', 
            'name', 
            'status', 
            'species', 
            'type', 
            'gender', 
            'image', 
            'is_custom',
            'is_active',
            'origin',
            'origin_detail', 
            'location', 
            'location_detail', 
            'episodes', 
            'episodes_detail'
        ]
        read_only_fields = ['character_id', 'is_custom', 'origin_detail', 'location_detail', 'episodes_detail']
        extra_kwargs = {
            'image': {'required': False, 'allow_blank': True},
            'type': {'required': False, 'allow_blank': True},
            'gender': {'required': False, 'allow_blank': True},
        }