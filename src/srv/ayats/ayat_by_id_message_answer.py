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

from app_types.update import Update
from db.connection import database
from integrations.tg.chat_id import TgChatId
from integrations.tg.tg_answers import TgAnswer, TgAnswerMarkup, TgTextAnswer
from srv.ayats.ayat import Ayat
from srv.ayats.ayat_callback_template_enum import AyatCallbackTemplateEnum
from srv.ayats.ayat_favorite_keyboard_button import AyatFavoriteKeyboardButton
from srv.ayats.favorites.ayat_is_favor import AyatIsFavor
from srv.ayats.neighbor_ayat_keyboard import NeighborAyatKeyboard
from srv.ayats.neighbor_ayats import PgNeighborAyats


@final
@attrs.define(frozen=True)
@elegant
class AyatByIdMessageAnswer(TgAnswer):
    """Текстовый ответ на поиск аята."""

    _result_ayat: Ayat
    _message_answer: TgAnswer

    async def build(self, update: Update) -> list[httpx.Request]:
        """Сборка ответа.

        :param update: Update
        :return: list[httpx.Request]
        """
        return await TgAnswerMarkup(
            TgTextAnswer(
                self._message_answer,
                await self._result_ayat.text(),
            ),
            AyatFavoriteKeyboardButton(
                NeighborAyatKeyboard(
                    PgNeighborAyats(database, await self._result_ayat.identifier().id()),
                    AyatCallbackTemplateEnum.get_ayat,
                ),
                AyatIsFavor(
                    self._result_ayat,
                    TgChatId(update),
                    database,
                ),
                self._result_ayat,
            ),
        ).build(update)
