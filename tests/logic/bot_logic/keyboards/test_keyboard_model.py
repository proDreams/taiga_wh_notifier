from src.logic.bot_logic.keyboards.keyboard_model import KeyboardGenerator


class TestKeyboardGeneratorClass:
    def test_create_keyboard(self, keyboard: KeyboardGenerator = KeyboardGenerator()):
        result_keyboard = keyboard.create_static_keyboard(key="started_keyboard", lang="en")

        assert "get_start" == result_keyboard.keyboard[0][0].text
