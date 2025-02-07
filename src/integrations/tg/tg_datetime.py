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
from typing import final

import attrs
import pytz
from pyeo import elegant

from app_types.date_time import DateTimeInterface
from app_types.update import Update
from exceptions.base_exception import InternalBotError
from services.json_path_value import ErrRedirectJsonPath, JsonPathValue


@final
@attrs.define(frozen=True)
@elegant
class TgDateTime(DateTimeInterface):
    """Время сообщения."""

    _update: Update

    def datetime(self) -> datetime.datetime:
        """Дата/время.

        :return: datetime.datetime
        """
        return datetime.datetime.fromtimestamp(
            int(
                ErrRedirectJsonPath(
                    JsonPathValue(
                        self._update.dict(),
                        '$..date',
                    ),
                    InternalBotError(),
                ).evaluate(),
            ),
            tz=pytz.timezone('UTC'),
        )
