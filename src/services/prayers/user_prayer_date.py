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
import datetime
from typing import SupportsInt, final

import attrs
from databases import Database
from pyeo import elegant

from app_types.date_time import AsyncDateTimeInterface
from exceptions.internal_exceptions import UserHasNotGeneratedPrayersError


@final
@attrs.define(frozen=True)
@elegant
class UserPrayerDate(AsyncDateTimeInterface):
    """Объект времени намаза привязанного к пользователю."""

    _user_prayer_id: SupportsInt
    _database: Database

    async def datetime(self) -> datetime.datetime:
        """Дата.

        :return: datetime.date
        :raises UserHasNotGeneratedPrayersError: если времня намаза не найдено
        """
        query = """
            SELECT day_id
            FROM prayers_at_user AS pau
            INNER JOIN prayers AS p ON pau.prayer_id = p.prayer_id
            WHERE prayer_at_user_id = :user_prayer_id
        """
        row = await self._database.fetch_one(query, {'user_prayer_id': int(self._user_prayer_id)})
        if not row:
            raise UserHasNotGeneratedPrayersError
        return row['day_id']
