import requests
from .models import Character, Location, Episode

"""
    @AUTHOR: Ivan Sanchez
    @LAST_UPDATE: 2026-09-19
    @DESCRIPTION: Servicio para obtener y almacenar personajes de la API de Rick and Morty.
                Garantiza sincronizar un número objetivo (p. ej. 200) de personajes de la API externa
                sin sobreescribir los registros personalizados (is_custom=True).
"""
#* Función para obtener y almacenar personajes de la API de Rick and Morty.
def fetch_and_save_characters(target_count=200):
    url = "https://rickandmortyapi.com/api/character"
    processed_count = 0
    new_added_count = 0  

    while url and processed_count < target_count:
        #* Realizamos la solicitud a la API externa para obtener los personajes.
        response = requests.get(url)
        if response.status_code != 200:
            break

        data = response.json()
        results = data.get('results', [])

        #* Iteramos sobre cada personaje obtenido de la API externa.
        for item in results:
            if processed_count >= target_count:
                break

            #* Obtenemos el ID del personaje de la API externa.
            character_id = item['id']

            #* Verificamos si el personaje ya existe en la base de datos.
            existing_character = Character.objects.filter(character_id=character_id).first()
            if existing_character and existing_character.is_custom:
                continue

            #* Determinamos el estado activo del personaje basado en si ya existía en la base de datos.
            is_active_status = existing_character.is_active if existing_character else True

            #* Procesamos la ubicación de origen del personaje
            origin_obj = None
            if item.get('origin') and item['origin'].get('url'):
                origin_id = int(item['origin']['url'].split('/')[-1])
                origin_obj, _ = Location.objects.get_or_create(
                    location_id=origin_id,
                    defaults={'name': item['origin']['name'], 'url': item['origin']['url']}
                )

            #* Procesamos la ubicación del personaje
            location_obj = None
            if item.get('location') and item['location'].get('url'):
                loc_id = int(item['location']['url'].split('/')[-1])
                location_obj, _ = Location.objects.get_or_create(
                    location_id=loc_id,
                    defaults={'name': item['location']['name'], 'url': item['location']['url']}
                )

            #* Capturamos 'created' que indica si el personaje se insertó como nuevo
            character, created = Character.objects.update_or_create(
                character_id=character_id,
                defaults={
                    'name': item['name'],
                    'status': item['status'],
                    'species': item['species'],
                    'type': item.get('type', ''),
                    'gender': item.get('gender', ''),
                    'image': item['image'],
                    'origin': origin_obj,
                    'location': location_obj,
                    'is_custom': False,
                    'is_active': is_active_status
                }
            )

            #* Si es un registro nuevo en BD, incrementamos el contador
            if created:
                new_added_count += 1

            #* Procesamos los episodios asociados al personaje.
            episode_objects = []
            for ep_url in item.get('episode', []):
                ep_id = int(ep_url.split('/')[-1])
                ep_obj, _ = Episode.objects.get_or_create(
                    episode_id=ep_id,
                    defaults={'name': f"Episode {ep_id}", 'episode': f"EP-{ep_id}", 'url': ep_url}
                )
                episode_objects.append(ep_obj)

            #* Asociamos los episodios al personaje en la base de datos.
            character.episodes.set(episode_objects)
            processed_count += 1

        #* Fin del bucle principal de procesamiento de personajes.  
        url = data.get('info', {}).get('next')

    #* Devolvemos un diccionario con ambos contadores
    return {
        'processed_characters': processed_count,
        'new_characters_added': new_added_count
    }