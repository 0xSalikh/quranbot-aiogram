# Требования к подкастам

## Получить подкаст в боте:

Если пользователь присылает сообщение "Подкасты" ему должен возвращаться случайный подкаст

Бот должен отправлять подкасты по идентификатору файла в телеграм https://core.telegram.org/bots/api#sendaudio 

Стандартная клавиатура должна содержать кнопку "🎧 Подкасты"

Вариации текста сообщения для получения подкаста:

 - Подкасты
 - подкасты
 - 🎧 Подкасты

## Парсинг подкастов

Парсер собирает подкасты со страницы https://umma.ru/audlo/shamil-alyautdinov/

Парсер запускается каждую неделю в понедельник, скачивает аудио, отправляет его в телеграм и сохраняет `file_id`
