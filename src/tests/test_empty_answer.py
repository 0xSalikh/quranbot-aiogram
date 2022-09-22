from integrations.tg.tg_answers import TgEmptyAnswer
from integrations.tg.tg_answers.update import Update


async def test():
    got = await TgEmptyAnswer('some_token').build(Update(update_id=32348))

    assert len(got) == 1
    assert got[0].url == 'https://api.telegram.org/botsome_token/'
