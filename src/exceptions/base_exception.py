class BaseAppError(Exception):
    """Базовое исключение бота."""

    user_message: str = 'Произошла какая-то ошибка'
    admin_message: str

    def __init__(self, answer_message: str | None = None, message_for_admin_text: str | None = None):
        if answer_message:
            self.user_message = answer_message  # noqa: WPS601
        # TODO: get traceback
        self.admin_message = message_for_admin_text or ''


class InternalBotError(BaseAppError):
    """Внутренняя ошибка бота."""

    user_message = ''
