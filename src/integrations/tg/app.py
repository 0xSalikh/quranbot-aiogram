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
import asyncio
from typing import final

import httpx
from databases import Database
from loguru import logger

from app_types.runable import Runable
from exceptions.base_exception import InternalBotError
from integrations.tg.polling_updates import PollingUpdatesIterator
from integrations.tg.sendable import SendableInterface


@final
class PollingApp(Runable):
    """Приложение на long polling."""

    def __init__(self, updates: PollingUpdatesIterator, sendable: SendableInterface):
        """Конструктор класса.

        :param updates: PollingUpdatesIterator
        :param sendable: SendableInterface
        """
        self._sendable = sendable
        self._updates = updates

    async def run(self) -> None:
        """Запуск."""
        logger.info('Start app on polling')
        async for update_list in self._updates:
            for update in update_list:
                logger.debug('Update: {update}', update=update)
                asyncio.ensure_future(self._sendable.send(update))
                await asyncio.sleep(0.1)


@final
class AppWithGetMe(Runable):
    """Объект для запуска с предварительным запросом getMe."""

    def __init__(self, origin: Runable, token: str):
        """Конструктор класса.

        :param origin: Runable
        :param token: str
        """
        self._origin = origin
        self._token = token

    async def run(self) -> None:
        """Запуск.

        :raises InternalBotError: в случае не успешного запроса к getMe
        """
        async with httpx.AsyncClient() as client:
            response = await client.get('https://api.telegram.org/bot{0}/getMe'.format(self._token))
            if response.status_code != httpx.codes.OK:
                raise InternalBotError(response.text)
            logger.info(response.content)
        await self._origin.run()


@final
class DatabaseConnectedApp(Runable):
    """Декоратор для подключения к БД."""

    def __init__(self, database: Database, app: Runable) -> None:
        """Конструктор класса.

        :param database: Database
        :param app: Runnable
        """
        self._database = database
        self._app = app

    async def run(self):
        """Запуск."""
        await self._database.connect()
        await self._app.run()
