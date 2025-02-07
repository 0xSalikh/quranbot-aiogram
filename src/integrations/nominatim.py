"""The MIT License (MIT).

Copyright (c) 2018-2023 Almaz Ilaletdinov <a.ilaletdinov@yandex.ru>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
OR OTHER DEALINGS IN THE SOFTWARE.
"""
from typing import Protocol, final

import attrs
import httpx
from pyeo import elegant

from integrations.tg.coordinates import Coordinates


@elegant
class CityName(Protocol):
    """Интерфейс интеграции с геосервисом."""

    async def search(self) -> str:
        """Поиск по координатам."""


@final
@attrs.define(frozen=True)
@elegant
class NominatimCityName(CityName):
    """Интеграция с https://nominatim.openstreetmap.org ."""

    _coordinates: Coordinates

    async def search(self) -> str:
        """Поиск по координатам.

        curl https://nominatim.openstreetmap.org/reverse.php?lat=55.7887&lon=49.1221&format=jsonv2

        :returns: CityName
        """
        url_template = 'https://nominatim.openstreetmap.org/reverse.php?lat={latitude}&lon={longitude}&format=jsonv2'
        url = url_template.format(
            latitude=self._coordinates.latitude(),
            longitude=self._coordinates.longitude(),
        )
        async with httpx.AsyncClient() as http_client:
            response = await http_client.get(url)
        return response.json()['address']['city']
