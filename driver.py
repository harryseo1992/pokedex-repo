# Name: Jesse & Harry
# Student number: A01240893, A01229209
from pokeretriever import cli_parser
from pokeretriever.cli_parser import InvalidModeException
from pokefacade import PokeFacade
import platform
from pokeretriever.pokemon_parser import PokemonParser
from pokeretriever.pokemon_requests import Request
import asyncio


def print_all(pokemon_data):
    for pokemon in pokemon_data:
        print(pokemon)


def write_all(output_name, pokemon_data):
    requests_len = len(pokemon_data)
    for pokemon in pokemon_data:
        PokemonParser.write_pokedex_object_to_output_file(requests_len, pokemon, output_name)


async def main():
    try:
        arguments = cli_parser.parse_request_requirements()
        output = arguments[-1]
        request = Request(*arguments)

        request_tasks, length = PokeFacade.execute_request(request)
        pokemon_data = await asyncio.gather(*request_tasks)

        if output:
            write_all(output, pokemon_data)
        else:
            print_all(pokemon_data)

    except InvalidModeException as e:
        print(e)


if __name__ == '__main__':
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
