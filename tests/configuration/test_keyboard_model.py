from src.core.settings import Configuration
from src.logic.bot_logic.keyboards.keyboards_stash import started_keyboard


class TestKeyboardGeneratorClass:
    target_class = Configuration

    def test_create_keyboard(self):
        expected_started_keyboard = self.target_class.keyboards.create_keyboard(
            keys=["get_start"], keyboard_type="reply", row_width=1
        )

        result_keyboard = started_keyboard

        assert expected_started_keyboard == result_keyboard
