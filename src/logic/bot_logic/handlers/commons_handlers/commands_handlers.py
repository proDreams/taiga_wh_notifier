from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from src.core.settings import Configuration
from src.entities.callback_classes.Pagination import Pagination
from src.logic.bot_logic.keyboards.keyboard_model import KeyboardGenerator

logger = Configuration.logger.get_logger(name=__name__)

main_router = Router()


@main_router.message(F.text == "/start")
async def start_handler(message: Message, keyboard: KeyboardGenerator = KeyboardGenerator()) -> None:
    """
    Handles the '/start' command by sending a welcome message.

    :param keyboard:
    :param message: The incoming message object containing the '/start' command.
    :type message: Message
    """
    await message.answer(
        Configuration.strings.get("messages_text").get("message_to_start"),
        reply_markup=keyboard.create_static_keyboard(key="started_keyboard", lang="en"),
    )

    # TODO: пока что это останется тут для тестов, потом уберем.
    # await message.answer(
    #     Configuration.strings.get("messages_text").get("message_to_start"),
    #     reply_markup=keyboard.create_dynamic_keyboard(buttons_dict=buttons_dict, key_in_storage="buttons_dict", lang="en"),
    # )


@main_router.callback_query(F.data == "menu")
async def main_menu_handler(callback: CallbackQuery, keyboard: KeyboardGenerator = KeyboardGenerator()) -> None:
    """
    Handles the main menu callback query.

    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param keyboard: A generator for creating keyboards.
    :type keyboard: KeyboardGenerator
    """

    await callback.message.edit_text(
        Configuration.strings.get("messages_text").get("message_to_main_menu"),
        reply_markup=keyboard.create_static_keyboard(key="main_menu_keyboard", lang="en"),
    )


@main_router.callback_query(Pagination.filter())
async def paginate_keyboard(
    callback: CallbackQuery, keyboard: KeyboardGenerator = KeyboardGenerator(), callback_data: Pagination = Pagination
) -> None:
    page = callback_data.page
    key_in_storage = callback_data.key_in_storage

    example = keyboard.get_buttons_dict(key_in_storage=key_in_storage)
    await callback.message.edit_reply_markup(
        reply_markup=keyboard.create_dynamic_keyboard(
            buttons_dict=example, key_in_storage=key_in_storage, lang="en", page=page
        )
    )
    await callback.answer()


# TODO: добавить обработчик для кнопки `Назад`
# TODO: добавить Callback класс для кнопки `Назад`
