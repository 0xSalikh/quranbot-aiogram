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
from databases import Database
from pyeo import elegant

from services.regular_expression import IntableRegularExpression


@elegant
class PrayerStatusInterface(Protocol):
    """Объект, рассчитывающий данные кнопки для изменения статуса прочитанности намаза."""

    def user_prayer_id(self) -> int:
        """Рассчитать идентификатор времени намаза пользователя."""

    def change_to(self) -> bool:
        """Рассчитать статус времени намаза пользователя."""


@final
@attrs.define(frozen=True)
@elegant
class PrayerStatus(PrayerStatusInterface):
    """Объект, рассчитывающий данные кнопки для изменения статуса прочитанности намаза."""

    _source: str

    def user_prayer_id(self) -> int:
        """Рассчитать идентификатор времени намаза пользователя.

        :return: int
        """
        return int(IntableRegularExpression(self._source))

    def change_to(self) -> bool:
        """Рассчитать статус времени намаза пользователя.

        :return: bool
        """
        return 'not' not in self._source.split('(')[0]


@elegant
class UserPrayerStatusInterface(Protocol):
    """Интерфейс статуса прочитанности намаза."""

    async def change(self, prayer_status: PrayerStatus):
        """Изменить статус прочитанности.

        :param prayer_status: PrayerStatus
        """


@final
@attrs.define(frozen=True)
@elegant
class UserPrayerStatus(UserPrayerStatusInterface):
    """Статус прочитанности намаза."""

    _connection: Database

    async def change(self, prayer_status: PrayerStatus):
        """Изменить статус прочитанности.

        :param prayer_status: PrayerStatus
        """
        query = """
            UPDATE prayers_at_user
            SET is_read = :is_read
            WHERE prayer_at_user_id = :prayer_id
        """
        await self._connection.execute(query, {
            'is_read': prayer_status.change_to(),
            'prayer_id': prayer_status.user_prayer_id(),
        })
