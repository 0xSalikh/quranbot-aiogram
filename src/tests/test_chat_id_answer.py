from integrations.tg.tg_answers import TgEmptyAnswer, TgChatIdAnswer
from integrations.tg.tg_answers.update import Update


async def test():
    got = await TgChatIdAnswer(
        TgEmptyAnswer('some_token'),
        348975,
    ).build(Update(update_id=32348))

    assert len(got) == 1
    assert got[0].url.query.decode('utf-8') == 'chat_id=348975'
