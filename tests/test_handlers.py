from unittest.mock import patch

from conftest import make_message, call_handler
from handlers import talk_to_me


@patch('handlers.get_or_create_user', return_value={'emoji': ':panda_face:'})
def test_talk_to_me(updater, effective_user):
    message = make_message('Проверка бота!', effective_user, updater.bot)
    call_handler(updater, talk_to_me, message)
    assert message.reply_text.called
    args, kwargs = message.reply_text.call_args
    assert args[0] == 'Проверка бота! :panda_face:'
    assert 'reply_markup' in kwargs
