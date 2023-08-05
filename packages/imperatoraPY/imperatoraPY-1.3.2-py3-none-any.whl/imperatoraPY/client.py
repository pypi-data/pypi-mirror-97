"""
MIT License

Copyright (c) 2020 Myer

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from . import request
from . import objects


get_entities = {
    "players": objects.Player,
    "towns": objects.Town,
}


class ImperatorClient:
    def __init__(self, api: str):
        self.api = api
        self.fetch = Fetch(api)

    async def status(self):
        status = await request.get(self.api, "status")
        return objects.Status(status)

    async def get(self, entity, entities, id_):
        construct = get_entities.get(entities, dict)
        entities = await request.get(self.api, f"get/{entities}/in/{entity}", id=id_)
        return [construct(entity) for entity in entities]


async def Imperator(api: str) -> ImperatorClient:
    """
    Class factory for ImperatorClient Objects
    TODO: Implement a request to /status that acts as an API key check and error if the request failed
    :param api: Imperator API key
    :return:
    """
    client = ImperatorClient(api)
    _ = await client.status()  # this acts as a check to see if the API key is invalid and errors if it is
    return client


class Fetch:
    def __init__(self, api: str):
        self.api = api

    async def player(self, *, name: str = None, uuid: str = None):
        """
        Fetches a player based off a username or UUID. If both are provided, the UUID is prioritized.
        :param name: The name of the player
        :param uuid: The UUID of the player
        :return: Player
        """
        player = await request.get(self.api, "fetch/player", username=name, uuid=uuid)
        return objects.Player(player)

    async def nation(self, *, name: str = None, id_: int = None):
        """
        Fetches a nation based off a name or ID. If both are provided, the ID is prioritized.
        :param name: The name of the nation
        :param id_: The ID of the nation
        :return: Nation
        """
        nation = await request.get(self.api, "fetch/nation", name=name, id=id_)
        return objects.Nation(nation)

    async def town(self, *, name: str = None, id_: int = None):
        """
        Fetches a town based off a name or ID. If both are provided, the ID is prioritized.
        :param name: The name of the town
        :param id_: The ID of the town
        :return: town
        """
        town = await request.get(self.api, "fetch/town", name=name, id=id_)
        return objects.Town(town)
