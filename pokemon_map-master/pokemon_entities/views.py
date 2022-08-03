import folium
from .models import Pokemon, PokemonEntity
from django.shortcuts import render
from django.utils.timezone import localtime
import logging

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)
logging.basicConfig(level=logging.DEBUG)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemons_db = Pokemon.objects.all()
    current_pokemons = PokemonEntity.objects.filter(appeared_at__lt=localtime(), disappeared_at__gt=localtime())
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon in current_pokemons:
        add_pokemon(
            folium_map, pokemon.lat,
            pokemon.lon,
            request.build_absolute_uri(pokemon.pokemon.image.url)
        )

    pokemons_on_page = []

    for pokemon in pokemons_db:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(pokemon.image.url),
            'title_ru': pokemon.title
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemon = {}
    pokemons = Pokemon.objects.get(id=pokemon_id)
    pokemon_entity = PokemonEntity.objects.get(id=pokemon_id)
    pokemon['pokemon_id'] = pokemons.id
    pokemon['img_url'] = request.build_absolute_uri(pokemons.image.url)
    pokemon['title_ru'] = pokemons.title
    pokemon['description'] = pokemons.description
    pokemon['title_en'] = pokemons.title_en
    pokemon['title_jp'] = pokemons.title_jp
    try:
        pokemon['previous_evolution'] = {
            'title_ru': pokemons.evolved_from.title,
            'pokemon_id': pokemons.evolved_from.id,
            'img_url': request.build_absolute_uri(pokemons.evolved_from.image.url)
        }
    except AttributeError:
        logging.info(f'У покемона {pokemons.title} нет предка')
    try:
        next_evolution = pokemons.next_evolution.all().first()
        pokemon['next_evolution'] = {
            'title_ru': next_evolution.title,
            'pokemon_id': next_evolution.id,
            'img_url': request.build_absolute_uri(next_evolution.image.url)
        }
    except AttributeError:
        logging.info(f'У покемона {pokemons.title} нет потомка')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    add_pokemon(
        folium_map, pokemon_entity.lat,
        pokemon_entity.lon,
        request.build_absolute_uri(pokemons.image.url)
    )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon
    })
