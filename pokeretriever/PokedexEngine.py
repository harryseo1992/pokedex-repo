"""
This file houses Pokemon, Ability, Move, and Stat Classes and other classes that are
parameters of those aforementioned four classes.
"""
import aiohttp
import abc
import json
import asyncio


class PokemonStat:
    """
    PokemonStat class represents the stat field of pokemon that will return Stat class if expanded option is true.
    """

    def __init__(self, name, base_value, url, is_expanded):
        self._name = name
        self._base_value = base_value
        self._url = url
        self._expanded_option = is_expanded

    async def handle_expanded(self):
        """
        Handles what stat information to return depending on expanded option.

        :return: Stat class object if expanded, dict if not
        """
        if self._expanded_option:
            return await self.expanded()
        else:
            return self.not_expanded()

    @staticmethod
    async def get_request(url, session: aiohttp.ClientSession):
        """
        Gets request for information and puts it in json form using aiohttp.

        :param url: String
        :param session: aiohttp.ClientSession() as session.
        :return: json
        """
        response = await session.request(method="GET", url=url)
        json_dict = await response.json()
        return json_dict

    async def expanded(self):
        """
        Uses self._url to query and return the results -> Should store Stat class object

        :return: Stat class object
        """
        async with aiohttp.ClientSession() as session:
            stuff = self.get_request(self._url, session)
            # async_task = asyncio.create_task(coroutine)
            response = await stuff
            return Stat(response['is_battle_only'], response['name'], response['id'])
        # If app is run with --expanded flag, then the URL provided must also be queried

    def not_expanded(self):
        """
        Returns dictionary form of info when not expanded.

        :return: dict
        """
        return {"Stat name": self._name, "Base value": self._base_value}

    def __str__(self):
        return f"Name: {self._name}\n" \
               f"Base value: {self._base_value}\n"


class PokemonAbility:
    """
    PokemonAbility represents the ability field of pokemon and has the option to expand that info using the url.
    """

    def __init__(self, name, url, is_expanded):
        self._name = name
        self._url = url
        self._expanded_option = is_expanded

    @staticmethod
    async def get_request(url, session: aiohttp.ClientSession):
        """
        Gets request for information and puts it in json form using aiohttp.

        :param url: String
        :param session: aiohttp.ClientSession() as session.
        :return: json
        """
        response = await session.request(method="GET", url=url)
        json_dict = await response.json()
        return json_dict

    async def handle_expanded(self):
        """
        Handles what stat information to return depending on expanded option.

        :return: Ability class object if expanded, dict if not
        """
        if self._expanded_option:
            return await self.expanded()
        else:
            return self.not_expanded()

    async def expanded(self):
        """
        Use self._url to query and return the results -> Should store Ability class object

        :return: Ability class object
        """
        async with aiohttp.ClientSession() as session:
            stuff = self.get_request(self._url, session)
            response = await stuff
            return Ability(response['generation']['name'], response['effect_entries'][1]['effect'],
                           response['effect_entries'][1]['short_effect'],
                           response['pokemon'], response['name'], response['id'])

    def not_expanded(self):
        """
        Returns dictionary form of info when not expanded.

        :return: dict
        """
        return {'Name': self._name}


class PokemonMove:
    """
    PokemonMove represents the move field of pokemon with option to expand that information using the url.
    """

    def __init__(self, name, level, url, is_expanded):
        self._name = name
        self._level = level
        self._url = url
        self._expanded_option = is_expanded

    @staticmethod
    async def get_request(url, session: aiohttp.ClientSession):
        """
        Gets request for information and puts it in json form using aiohttp.

        :param url: String
        :param session: aiohttp.ClientSession() as session.
        :return: json
        """
        response = await session.request(method="GET", url=url)
        json_dict = await response.json()
        return json_dict

    async def handle_expanded(self):
        """
        Handles what stat information to return depending on expanded option.

        :return: Move class object if expanded, dict if not
        """
        if self._expanded_option:
            return await self.expanded()
        else:
            return self.not_expanded()

    async def expanded(self):
        """
        Use self._url to query and return the results -> Should store Move class object

        :return: Move class object
        """
        async with aiohttp.ClientSession() as session:
            stuff = self.get_request(self._url, session)
            response = await stuff
            return Move(response['generation'], response['accuracy'],
                        response['pp'], response['power'], response['type'],
                        response['damage_class'], response['effect_entries'][0]['short_effect'],
                        response['name'], response['id'])
        # If app is run with --expanded flag, then the URL provided must also be queried

    def not_expanded(self):
        """
        Returns dictionary form of info when not expanded.

        :return: dict
        """
        return {'move_name': self._name, 'level_required': self._level}


class PokedexObject:
    """
    PokedexObject represents the return form of user's query: Pokemon, Move, or Ability
    """

    def __init__(self, name, object_id):
        self._name = name
        self._id = object_id


class PokedexObjectFactory(abc.ABC):
    """
    PokedexObjectFactory represents the factory that creates the PokedexObject that is required by query.
    """

    @abc.abstractmethod
    def create_object(self, response_json, request) -> PokedexObject:
        pass


class PokemonFactory(PokedexObjectFactory):
    """
    PokemonFactory represents the factory that will create Pokemon object which inherits from PokedexObject
    """

    async def create_object(self, response_json, request) -> PokedexObject:
        """
        Creates Pokemon class object using the response in json format and Request object.

        :param response_json: json
        :param request: Request class object
        :return: Pokemon class object
        """
        stats = await asyncio.gather(*[PokemonStat(stat['stat']['name'], stat['base_stat'], stat['stat']['url'],
                                                   request.is_expanded).handle_expanded()
                                       for stat in response_json['stats']])
        moves = await asyncio.gather(
            *[PokemonMove(move['move']['name'], move['version_group_details'][0]['level_learned_at'],
                          move['move']['url'], request.is_expanded).handle_expanded()
              for move in response_json['moves']])
        abilities = await asyncio.gather(*[PokemonAbility(ability['ability']['name'], ability['ability']['url'],
                                                          request.is_expanded).handle_expanded()
                                           for ability in response_json['abilities']])
        return Pokemon(response_json['height'], response_json['weight'],
                       stats, response_json['types'],
                       abilities, moves,
                       request.is_expanded, response_json['name'], response_json['id'])


class MoveFactory(PokedexObjectFactory):
    """
    MoveFactory represents the factory that will create Move object which inherits from PokedexObject
    """

    def create_object(self, response_json, request) -> PokedexObject:
        """
        Creates Move class object using the response in json format and Request object.

        :param response_json: json
        :param request: Request class object
        :return: Move class object
        """
        return Move(response_json['generation'], response_json['accuracy'],
                    response_json['pp'], response_json['power'], response_json['type'],
                    response_json['damage_class'], response_json['effect_entries'][0]['short_effect'],
                    response_json['name'], response_json['id'])


class AbilityFactory(PokedexObjectFactory):
    """
    AbilityFactory represents the factory that will create Ability object which inherits from PokedexObject
    """

    def create_object(self, response_json, request) -> PokedexObject:
        """
        Creates Ability class object using the response in json format and Request object.

        :param response_json: json
        :param request: Request class object
        :return: Ability class object
        """
        return Ability(response_json['generation']['name'],
                       response_json['effect_entries'][1]['effect'],
                       response_json['effect_entries'][1]['short_effect'],
                       response_json['pokemon'], response_json['name'], response_json['id'])


class Pokemon(PokedexObject):
    """
    Pokemon class represents the Pokemon information that one gets when querying for certain pokemon/pokemon id.
    """

    def __init__(self, height, weight, stats, types, abilities, moves, is_expanded, *basic_pokedex_info):
        super().__init__(*basic_pokedex_info)
        self._height = height
        self._weight = weight
        self._stats = stats
        self._types = types
        self._abilities = abilities
        self._moves = moves
        self._expanded_option = is_expanded

    def __str__(self):
        stats = json.dumps([stat.__dict__ if self._expanded_option else stat for stat in self._stats],
                           sort_keys=False, indent=4)
        abilities = json.dumps([ability.__dict__ if self._expanded_option else ability for ability in self._abilities],
                               sort_keys=False, indent=4)
        moves = json.dumps([move.__dict__ if self._expanded_option else move for move in self._moves],
                           sort_keys=False, indent=4)
        return f"Pokemon: {self._name}\n" \
               f"Height: {self._height} decimetres\n" \
               f"Weight: {self._weight} hectograms\n" \
               f"Stats: {stats}\n" \
               f"Types: {self._types}\n" \
               f"Abilities: {abilities}\n" \
               f"Moves: {moves}\n"


class Ability(PokedexObject):
    """
    Ability class represents the Ability information that one gets when querying for certain ability/ability id.
    """

    def __init__(self, generation, effect, effect_short, pokemons, *basic_pokedex_info):
        super().__init__(*basic_pokedex_info)
        self._generation = generation
        self._effect = effect
        self._effect_short = effect_short
        self._pokemons = [pokemon['pokemon']['name'] for pokemon in pokemons]  # list of strings

    def __str__(self):
        return f"Name: {self._name}\n" \
               f"ID: {self._id}\n" \
               f"Generation: {self._generation}\n" \
               f"Effect: {self._effect}\n" \
               f"Short Effect: {self._effect_short}\n" \
               f"Pokemons: {self._pokemons}\n"


class Stat(PokedexObject):
    """
    Stat class represents the stat information that user gets when querying for certain stat/stat id.
    """

    def __init__(self, is_battle_only, *basic_pokedex_info):
        super().__init__(*basic_pokedex_info)
        self._is_battle_only = is_battle_only

    def __str__(self):
        return f"Name: {self._name}\n" \
               f"ID: {self._id}\n" \
               f"Is Battle Only: {self._is_battle_only}\n"


class Move(PokedexObject):
    """
    Move class represents the move information that user gets when querying for certain move/move id.
    """

    def __init__(self, generation, accuracy, pp, power, move_type, damage_class, effect_short, *basic_pokedex_info):
        super().__init__(*basic_pokedex_info)
        self._generation = generation
        self._accuracy = accuracy
        self._pp = pp
        self._power = power
        self._type = move_type
        self._damage_class = damage_class
        self._effect_short = effect_short

    def __str__(self):
        return f"Name: {self._name}\n" \
               f"ID: {self._id}\n" \
               f"Generation: {self._generation}\n" \
               f"Accuracy: {self._accuracy}\n" \
               f"PP: {self._pp}\n" \
               f"Power: {self._power}\n" \
               f"Type: {self._type}\n" \
               f"Damage Class: {self._damage_class}\n" \
               f"Short Effect: {self._effect_short}\n"
