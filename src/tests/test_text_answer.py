from integrations.tg.tg_answers import TgEmptyAnswer, TgTextAnswer
from integrations.tg.tg_answers.update import Update


async def test():
    got = await TgTextAnswer(
        TgEmptyAnswer('some_token'),
        'message',
    ).build(Update(update_id=32348))

    assert len(got) == 1
    assert got[0].url.query.decode('utf-8') == 'text=message'
