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

import httpx
from databases import Database
from redis.asyncio import Redis

from app_types.update import Update
from handlers.favorites_answer import FavoriteAyatsAnswer
from handlers.full_start_answer import FullStartAnswer
from handlers.podcast_answer import PodcastAnswer
from handlers.prayer_time_answer import PrayerTimeAnswer
from handlers.search_ayat_by_keyword_answer import SearchAyatByKeywordAnswer
from handlers.search_ayat_by_numbers_answer import SearchAyatByNumbersAnswer
from handlers.search_city_answer import SearchCityAnswer
from handlers.status_answer import StatusAnswer
from handlers.user_prayer_status_change_answer import UserPrayerStatusChangeAnswer
from integrations.nats_integration import SinkInterface
from integrations.tg.tg_answers import (
    TgAnswer,
    TgAnswerFork,
    TgAnswerToSender,
    TgAudioAnswer,
    TgCallbackQueryRegexAnswer,
    TgEmptyAnswer,
    TgHtmlParseAnswer,
    TgKeyboardEditAnswer,
    TgMessageAnswer,
    TgMessageRegexAnswer,
    TgTextAnswer,
)
from repository.admin_message import AdminMessage
from repository.podcast import RandomPodcast
from repository.prayer_time import UserPrayers
from services.answers.change_state_answer import ChangeStateAnswer
from services.answers.safe_fork import SafeFork
from services.city.inline_query_answer import InlineQueryAnswer
from services.city.search import SearchCityByName
from services.help_answer import HelpAnswer
from services.prayers.invite_set_city_answer import InviteSetCityAnswer
from services.prayers.prayer_status import UserPrayerStatus
from services.state_answer import StepAnswer
from services.user_state import UserStep
from settings import settings
from srv.ayats.ayat_by_id_answer import AyatByIdAnswer
from srv.ayats.change_favorite_ayat_answer import ChangeFavoriteAyatAnswer
from srv.ayats.favorite_ayat_page import FavoriteAyatPage
from srv.ayats.highlighted_search_answer import HighlightedSearchAnswer
from srv.ayats.search_ayat_by_text_callback_answer import SearchAyatByTextCallbackAnswer


@final
class QuranbotAnswer(TgAnswer):
    """Ответ бота quranbot."""

    def __init__(
        self,
        database: Database,
        redis: Redis,
        event_sink: SinkInterface,
    ):
        """Конструктор класса.

        :param database: Database
        :param redis: Redis
        :param event_sink: SinkInterface
        """
        self._database = database
        self._redis = redis
        self._event_sink = event_sink
        self._pre_build()

    async def build(self, update: Update) -> list[httpx.Request]:
        """Сборка ответа.

        :param update: Update
        :return: list[httpx.Request]
        """
        return await self._answer.build(update)

    def _pre_build(self) -> None:
        empty_answer = TgEmptyAnswer(settings.API_TOKEN)
        # TODO: перенести сборку этих классов в хендлеры
        answer_to_sender = TgAnswerToSender(TgMessageAnswer(empty_answer))
        audio_to_sender = TgAnswerToSender(TgAudioAnswer(empty_answer))
        html_to_sender = TgAnswerToSender(
            TgHtmlParseAnswer(
                TgMessageAnswer(empty_answer),
            ),
        )
        self._answer = SafeFork(
            TgAnswerFork(
                TgMessageRegexAnswer(
                    'Подкасты',
                    PodcastAnswer(settings.DEBUG, empty_answer, RandomPodcast(self._database), self._redis),
                ),
                TgMessageRegexAnswer(
                    'Время намаза',
                    PrayerTimeAnswer(self._database, self._redis, empty_answer),
                ),
                TgMessageRegexAnswer(
                    'Избранное',
                    FavoriteAyatsAnswer(settings.DEBUG, self._database, self._redis, empty_answer),
                ),
                StepAnswer(
                    UserStep.city_search.value,
                    SearchCityAnswer(self._database, empty_answer, settings.DEBUG, self._redis),
                    self._redis,
                ),
                TgMessageRegexAnswer(
                    r'\d+:\d+',
                    SearchAyatByNumbersAnswer(settings.DEBUG, empty_answer, self._redis),
                ),
                TgMessageRegexAnswer(
                    'Найти аят',
                    ChangeStateAnswer(
                        TgTextAnswer(answer_to_sender, 'Введите слово для поиска:'),
                        self._redis,
                        UserStep.ayat_search,
                    ),
                ),
                TgMessageRegexAnswer(
                    'Поменять город',
                    InviteSetCityAnswer(
                        TgTextAnswer(answer_to_sender, 'Отправьте местоположение или воспользуйтесь поиском'),
                        self._redis,
                    ),
                ),
                TgMessageRegexAnswer(
                    '/start',
                    FullStartAnswer(self._database, empty_answer, self._event_sink, self._redis),
                ),
                TgMessageRegexAnswer(
                    '/status',
                    StatusAnswer(empty_answer, self._database, self._redis),
                ),
                TgMessageRegexAnswer(
                    '/help',
                    HelpAnswer(html_to_sender, AdminMessage('start', self._database), self._redis),
                ),
                StepAnswer(
                    UserStep.ayat_search.value,
                    SearchAyatByKeywordAnswer(
                        settings.DEBUG, html_to_sender, audio_to_sender, answer_to_sender, self._redis,
                    ),
                    self._redis,
                ),
                TgCallbackQueryRegexAnswer(
                    '(mark_readed|mark_not_readed)',
                    UserPrayerStatusChangeAnswer(
                        TgAnswerToSender(
                            TgKeyboardEditAnswer(empty_answer),
                        ),
                        UserPrayerStatus(self._database),
                        UserPrayers(self._database),
                    ),
                ),
                TgCallbackQueryRegexAnswer(
                    'getAyat',
                    AyatByIdAnswer(
                        settings.DEBUG,
                        html_to_sender,
                        audio_to_sender,
                    ),
                ),
                StepAnswer(
                    UserStep.ayat_search.value,
                    TgCallbackQueryRegexAnswer(
                        'getSAyat',
                        HighlightedSearchAnswer(
                            SearchAyatByTextCallbackAnswer(
                                settings.DEBUG,
                                html_to_sender,
                                audio_to_sender,
                                self._redis,
                            ),
                            self._redis,
                        ),
                    ),
                    self._redis,
                ),
                TgCallbackQueryRegexAnswer(
                    'getFAyat',
                    FavoriteAyatPage(
                        settings.DEBUG,
                        html_to_sender,
                        audio_to_sender,
                    ),
                ),
                TgCallbackQueryRegexAnswer(
                    '(addToFavor|removeFromFavor)',
                    ChangeFavoriteAyatAnswer(
                        self._database,
                        answer_to_sender,
                    ),
                ),
                InlineQueryAnswer(
                    empty_answer,
                    SearchCityByName(self._database),
                ),
            ),
            TgAnswerToSender(
                TgMessageAnswer(empty_answer),
            ),
        )
