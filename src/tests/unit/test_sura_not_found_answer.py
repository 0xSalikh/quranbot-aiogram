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
from typing import final

import attrs
import httpx
from pyeo import elegant

from app_types.update import FkUpdate, Update
from exceptions.content_exceptions import SuraNotFoundError
from integrations.tg.tg_answers import TgAnswer
from srv.ayats.sura_not_found_safe_answer import SuraNotFoundSafeAnswer


@attrs.define(frozen=True)
@elegant
@final
class ThroughDomainAnswer(TgAnswer):

    _domain: str

    async def build(self, update: Update) -> list[httpx.Request]:
        return [httpx.Request('GET', self._domain)]


@elegant
@final
class SuraNotFoundAnswer(TgAnswer):

    async def build(self, update):
        raise SuraNotFoundError


async def test_normal_flow():
    got = await SuraNotFoundSafeAnswer(
        ThroughDomainAnswer('https://normal.flow'),
        ThroughDomainAnswer('https://error.flow'),
    ).build(FkUpdate())

    assert got[0].url == 'https://normal.flow'


async def test_error_flow():
    got = await SuraNotFoundSafeAnswer(
        SuraNotFoundAnswer(),
        ThroughDomainAnswer('https://error.flow'),
    ).build(FkUpdate())

    assert 'error.flow' in str(got[0].url)
