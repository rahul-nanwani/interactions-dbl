# MIT License
#
# Copyright (c) 2022 Rahul Nanwani
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""DBLClient Module"""

from asyncio import get_event_loop, sleep
from typing import Union, Any

from aiohttp import ClientSession, ClientResponse
from interactions import Client, Snowflake

from .exceptions import *

__all__ = ('DBLClient',)


class DBLClient:
    """This class is used to interact with the botblock.org API using a discord-py-interactions bot instance
    Find the supported bot listings on: https://botblock.org/lists
    Use the listing URL without https:// or http://

    :param bot: (interactions.Client) An instance of a discord-py-interactions Client object

    :keyword auth: (dict) List URL as key and the Token as the value
    :keyword interval: [Default: 1800] (int) interval in seconds between each auto posting of guild count
    :keyword auto_post: [Default: True] (bool) Set auto posting
    """

    __slots__ = (
        'api_base_url', 'session',
        'bot', 'auth', 'interval',
        'guild_count',
    )

    def __init__(self, bot: Client, **kwargs: Any):
        # default
        self.api_base_url: str = "https://botblock.org/api/"
        self.session: Union[ClientSession, None] = None

        # required input
        self.bot = bot
        self.auth: dict = kwargs.get('auth')

        # optional input
        self.interval: int = kwargs.get('interval', 1800)

        if kwargs.get('auto_post', True):
            get_event_loop().create_task(self._loop(self.interval))

    def __repr__(self) -> str:
        """Class instance representation"""

        return f"<DBLClient: {self.bot.me.name}>"

    @property
    def guild_count(self) -> int:
        """Gets the guild count from the bot"""

        return len(self.bot.guilds)

    def _session_init(self) -> None:
        """Starts up the aiohttp session if one does not yet exist"""

        if self.session is None:
            self.session = ClientSession()

    def _guild_count_body(self, bot_id: Snowflake, guild_count: int) -> dict:
        """Gets the body used for a server/guild count post API request

        :param bot_id: (Snowflake) The ID of the bot you want to update server/guild count for
        :param guild_count: (int) The server/guild count for the bot

        :return: (dict) the body to send
        """

        data = self.auth.copy()
        data["server_count"] = guild_count
        data["bot_id"] = str(bot_id)
        return data

    async def _handle_response(self, response: ClientResponse) -> dict:
        """Handles all responses returned from any API request

        :param response: (aiohttp.ClientResponse) The response from the aiohttp request to the API

        :return: (dict) The formatted response from the API endpoint

        :raises EmptyResponse: API No/Empty response
        :raises RateLimited: API rate limited
        :raises RequestFailure: API request failure
        """

        status = response.status
        text = await response.text()

        try:
            json = await response.json()
        except Exception:
            json = {}

        # EmptyResponse
        if not (json and text.strip()):
            raise EmptyResponse()

        # RateLimited
        elif status == 429:
            raise RateLimited(json)

        # RequestFailure
        elif status != 200:
            raise RequestFailure(status, text)

        else:
            return json

    async def _post_data(self, endpoint: str, content: Union[list, dict]) -> dict:
        """POST data to an API endpoint

        :param endpoint: (str) The endpoint to access on the API
        :param content: (Union[list, dict]) The data to be posted to the endpoint

        :return: (dict) The formatted response from the API endpoint
        """

        self._session_init()
        async with self.session.post(
                url=self.api_base_url + endpoint,
                json=content,
                headers={'content-type': 'application/json'}
        ) as response:
            return await self._handle_response(response)

    async def _post_guild_count(self, bot_id: Snowflake, guild_count: int) -> dict:
        """POST a server/guild count for a bot

        :param bot_id: (Snowflake) The ID of the bot you want to update server/guild count for
        :param guild_count: (int) The server/guild count for the bot

        :return: (dict) The response from the API endpoint
        """

        return await self._post_data("count", self._guild_count_body(bot_id, guild_count))

    async def _loop(self, interval: float) -> None:
        """The internal loop used for automatically posting server/guild count stats"""

        await self.bot.wait_until_ready()
        while True:
            await self.post_count()
            await sleep(interval)

    def add_auth(self, list_url: str, auth_token: str) -> None:
        """Sets an authorisation token for the given list URL from botblock.org

        :param list_url: (str) The URL of the list from botblock.org (without https:// or http://)
        :param auth_token: (str) The authorisation token this list provided you to use their API
        """

        self.auth[list_url] = auth_token

    def remove_auth(self, list_url: str) -> None:
        """Removes an authorisation token for the given list URL from botblock.org

        :param list_url: (str) The URL of the list from botblock.org (without https:// or http://)
        """

        if list_url in self.auth.keys():
            del self.auth[list_url]

    async def post_count(self) -> dict:
        """POST current server/guild count based on bot data

        :return: (str) The response from the API endpoint
        """

        return await self._post_guild_count(self.bot.me.id, self.guild_count)
