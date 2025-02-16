from unittest.mock import AsyncMock, patch

import pytest
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from aiogram.methods import DeleteMessage, EditMessageText
from aiogram.types import Message

from src.core.Base.exceptions import BotBlocked
from src.core.settings import Configuration
from src.utils.send_message_utils import send_message, try_delete


@pytest.mark.asyncio
class TestBotMethods:
    @pytest.fixture(autouse=True)
    def setup_mocks(self):
        self.mock_bot = AsyncMock()
        Configuration.bot = self.mock_bot

        self.logger_patcher = patch("src.utils.send_message_utils.logger")
        self.mock_logger = self.logger_patcher.start()

    async def test_try_delete_success(self):
        self.mock_bot.delete_message = AsyncMock()
        await try_delete(chat_id=123, message_id=456)
        self.mock_bot.delete_message.assert_awaited_once_with(123, 456)

    async def test_try_delete_bad_request(self):
        self.mock_bot.delete_message.side_effect = TelegramBadRequest(
            message="Bad Request", method=DeleteMessage(chat_id=123, message_id=456)
        )
        await try_delete(chat_id=123, message_id=456)
        self.mock_logger.warning.assert_called_once_with("Bad Request")

    async def test_try_delete_forbidden(self):
        self.mock_bot.delete_message.side_effect = TelegramForbiddenError(
            message="Forbidden", method=DeleteMessage(chat_id=123, message_id=456)
        )
        with pytest.raises(BotBlocked):
            await try_delete(chat_id=123, message_id=456)
        self.mock_logger.warning.assert_called_once_with("The bot is blocked by user: 123")

    async def test_send_message_success(self):
        mock_message = AsyncMock(spec=Message)
        self.mock_bot.send_message.return_value = mock_message
        result = await send_message(chat_id=123, text="Hello")
        assert result == mock_message
        self.mock_bot.send_message.assert_awaited_once_with(chat_id=123, text="Hello", reply_markup=None)

    async def test_send_message_try_to_edit_success(self):
        mock_message = AsyncMock(spec=Message)
        self.mock_bot.edit_message_text.return_value = mock_message
        result = await send_message(chat_id=123, text="Edited", message_id=456, try_to_edit=True)
        assert result == mock_message
        self.mock_bot.edit_message_text.assert_awaited_once_with(
            chat_id=123, message_id=456, text="Edited", reply_markup=None
        )

    async def test_send_message_try_to_edit_bad_request(self):
        self.mock_bot.edit_message_text.side_effect = TelegramBadRequest(
            message="Bad Request", method=EditMessageText(chat_id=123, message_id=456, text="New")
        )
        self.mock_bot.send_message = AsyncMock()
        await send_message(chat_id=123, text="New", message_id=456, try_to_edit=True)
        self.mock_logger.warning.assert_called_with("Bad Request")
        self.mock_bot.send_message.assert_awaited()

    async def test_send_message_try_to_edit_forbidden(self):
        self.mock_bot.edit_message_text.side_effect = TelegramForbiddenError(
            message="Forbidden", method=EditMessageText(chat_id=123, message_id=456, text="New")
        )
        result = await send_message(chat_id=123, text="New", message_id=456, try_to_edit=True)
        assert result is None
        self.mock_logger.warning.assert_called_with("The bot is blocked by user: 123")
