"""
utility functions

caches pokemon data
"""
import requests
import pathlib
import json
import appdirs
from requests.exceptions import ConnectionError
from json.decoder import JSONDecodeError
from .constants import pokedex_number_start, pokedex_number_end
from . import __version__

cache_directory = pathlib.Path(
    appdirs.user_cache_dir(
        appname="pokemon-yeet",
        appauthor=False,
        version=__version__,
    )
)


def setup_game():
    "download pokemon data"
    if not cache_directory.is_dir():
        print(f"Creating cache directory '{cache_directory.resolve()}'...")
        cache_directory.mkdir(parents=True)

    for i in range(pokedex_number_start, pokedex_number_end + 1):
        pokemon_json_file = cache_directory / f"{i}.json"

        if pokemon_json_file.is_file():
            # Pokemon already downloaded
            continue

        print(f"Downloading pokemon #{i}")

        error_message = f"cannot get pokemon #{i}"
        try:
            response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{i}')
        except ConnectionError:
            print(error_message)
            continue
        finally:
            response.close()

        if response.status_code != 200:
            print(error_message)
            continue

        try:
            pokemon_json = response.json()
        except JSONDecodeError:
            print(f"cannot decode json for pokemon #{i}")
            continue

        with pokemon_json_file.open(mode="wt") as file:
            json.dump(pokemon_json, file, indent=2, sort_keys=True)

    print("Pokemon data downloaded")


def load_pokemon(pokemon_number):
    "return the information for one pokemon"
    pokemon_json_file = cache_directory / f"{pokemon_number}.json"
    with pokemon_json_file.open(mode="rt") as file:
        data = json.load(file)

    poke_name = data['name']
    poke_type = data['types'][0]['type']['name']
    poke_hp = data['stats'][0]['base_stat']

    return poke_name, poke_type, poke_hp
