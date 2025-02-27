import pytest

from src.logic.bot_logic.keyboards.keyboard_generator import KeyboardGenerator


@pytest.mark.asyncio
class TestKeyboardGeneratorClass:
    async def test_create_keyboard(self):
        keyboard = KeyboardGenerator()
        result_keyboard = await keyboard.generate_static_keyboard(kb_key="start_keyboard", lang="en")

        assert "Menu" == result_keyboard.inline_keyboard[0][0].text
