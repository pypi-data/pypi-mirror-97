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

from . import exceptions
import aiohttp


URL = "https://imperator.network/api"


async def get(api: str, endpoint: str, **kwargs) -> dict:
    """
    Sends a get request to the last.fm API
    :param api: API key
    :param endpoint: API endpoint to access
    :param kwargs: Will be converted to HTTP attributes (?key=value&key=value)
    :return: dict (JSON) of the API response
    """
    parameters = "".join([f"&{key}={value}" for key, value in kwargs.items() if bool(value)])
    async with aiohttp.request("GET", f"{URL}/{endpoint}?key={api}{parameters}") as response:
        if response.status == 400:
            raise exceptions.BadRequestError
        if response.status == 401:
            raise exceptions.InvalidAPIKeyError
        if response.status == 429:
            raise exceptions.RatelimitExceededError
        return await response.json()
