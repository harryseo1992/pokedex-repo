"""
This module contains PokemonParser class that helps with returning PokedexObject for PokeFacade class.
"""
import aiohttp
from pokeretriever.PokedexEngine import PokemonFactory, AbilityFactory, MoveFactory
from pokeretriever.pokemon_requests import Modes
import datetime
import time
import os


class PokemonParser:
    """
    PokemonParser class represents the parser used by the PokeFacade to help get PokedexObject
    """
    SEARCH_MODE_MAPPER = {
        "pokemon": Modes.POKEMON.value,
        "ability": Modes.ABILITY.value,
        "move": Modes.MOVE.value,
    }

    FACTORY_MAPPER = {
        "pokemon": PokemonFactory(),
        "ability": AbilityFactory(),
        "move": MoveFactory()
    }

    def make_target_url(self, search_mode, content):
        """
        Makes target url from search mode and content.

        :param search_mode: String, Search mode in Request: pokemon, move, or ability
        :param content: String, name or id of query
        :return: String, target url to be used for API GET request.
        """
        return f"{self.SEARCH_MODE_MAPPER[search_mode]}/{content.strip()}"

    async def pokemon_data_request(self, request, target_url):
        """Parse a single pokemon request.

        :param request: Request object
        :param target_url: String, target url to make API GET request
        :return: PokedexObject class object
        """
        async with aiohttp.ClientSession() as session:
            try:
                response = await session.request("GET", url=target_url)
                response_json = await response.json()

                return self.FACTORY_MAPPER[request.search_mode].create_object(response_json, request)
            except Exception as e:
                if request.output:
                    with open(request.output, mode="a", encoding='utf-8') as file:
                        file.write(f"\nAn error has occurred. Skipping this request\n")
                else:
                    print(e)

    @staticmethod
    def write_pokedex_object_to_output_file(num_of_requests, pokedex_object, output):
        """
        Writes PokedexObject to output file.

        :param num_of_requests: Integer, number of requests.
        :param pokedex_object: PokedexObject class object
        :param output: String, output filepath
        :return: None
        """
        try:
            if (not os.path.exists(output)) or os.stat(output).st_size == 0:
                with open(output, mode="a", encoding='utf-8') as data_file:
                    data_file.write(f"Timestamp: "
                                    f"{datetime.datetime.fromtimestamp(time.time()).strftime('%d/%m/%Y %H:%M')}\n"
                                    f"Number of requests: {num_of_requests}\n\n")
        except Exception as e:
            print(e)
        finally:
            with open(output, mode="a", encoding='utf-8') as file:
                file.write(f"{str(pokedex_object)}\n")
            print("Printed, shipped, and finished!")
