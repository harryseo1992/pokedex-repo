"""
This module contains PokeFacade class that helps to execute requests under the hood.
"""
from pokeretriever.pokemon_requests import Request
from pokeretriever.pokemon_parser import PokemonParser


class PokeFacade:
    """
    PokeFacade represents the facade pattern where heavy duty operations are carried out under the hood.
    """
    @staticmethod
    def __execute_requests(request, inputs: list):
        """
        Executes the requests to get list of parsed tasks.

        :param inputs: name of input to retrieve from
        :return: List of tasks of Pokemon objects
        """
        pokemon_parser = PokemonParser()
        parse_tasks = []
        for content in inputs:
            target_url = pokemon_parser.make_target_url(request.search_mode, content)
            parse_task = pokemon_parser.pokemon_data_request(request, target_url)
            parse_tasks.append(parse_task)

        return parse_tasks

    @staticmethod
    def execute_request(request: Request) -> (list, int):
        """
        Executes request using the Request object to query for Pokemon, Ability, or Move.

        :param request: Request object
        :return: None, will either write to output file or print the results
        """
        is_single_item = request.input_data and not request.input_file

        if is_single_item:
            inputs = [request.input_data]
        else:
            with open(request.input_file, mode='r') as file:
                inputs = file.readlines()

        return PokeFacade.__execute_requests(request, inputs), len(inputs)
