from django.db import models

"""
AUTHOR: Ivan Sanchez
LAST_UPDATE: 2026-09-19
DESCRIPTION: Modelos para Character, Location y Episode
"""
class Location(models.Model):
    #* Modelo para representar una ubicación en el universo de Rick and Morty
    location_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=100, blank=True, null=True)
    dimension = models.CharField(max_length=100, blank=True, null=True)
    url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

class Episode(models.Model):
    #* Modelo para representar un episodio en el universo de Rick and Morty
    episode_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    air_date = models.CharField(max_length=100, blank=True, null=True)
    episode = models.CharField(max_length=50, help_text="Ejemplo: S01E01")
    url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.episode} - {self.name}"

class Character(models.Model):
    #* Modelo para representar un personaje en el universo de Rick and Morty
    character_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    species = models.CharField(max_length=100)
    type = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=50, blank=True, null=True)
    image = models.URLField()
    is_custom = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    #? Relaciones con Ubicaciones (ForeignKey -> Uno a Muchos)
    origin = models.ForeignKey(
        Location, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='characters_origin'
    )
    
    #? Relación con la ubicación actual del personaje (ForeignKey -> Uno a Muchos)
    location = models.ForeignKey(
        Location, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='characters_location'
    )

    #? Relación con los episodios en los que aparece el personaje (ManyToManyField -> Muchos a Muchos)
    episodes = models.ManyToManyField(
        Episode, 
        related_name='characters',
        blank=True
    )

    def __str__(self):
        return f"{self.name} ({'Modificado' if self.is_custom else 'Original'})"