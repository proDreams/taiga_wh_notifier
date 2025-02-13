import json

from src.entities.schemas.webhook_data.webhook_payload_schemas import WebhookPayload


class TestWebhookPayloadSchema:
    def test_webhook_payload_task(self):
        with open("tests/entities/fixtures/task_raw.json", encoding="utf-8") as f:
            input_data = json.load(f)
        # Валидируем входной JSON по схеме
        event = WebhookPayload.model_validate(input_data)
        # Получаем строковое представление модели (оно должно быть детерминированным)
        actual = str(event)
        with open("tests/entities/fixtures/expected_task.txt", encoding="utf-8") as f:
            expected = f.read().strip()
        assert actual == expected

    def test_webhook_payload_milestone(self):
        with open("tests/entities/fixtures/milestone_raw.json", encoding="utf-8") as f:
            input_data = json.load(f)
        event = WebhookPayload.model_validate(input_data)
        actual = str(event)
        with open("tests/entities/fixtures/expected_milestone.txt", encoding="utf-8") as f:
            expected = f.read().strip()
        assert actual == expected

    def test_webhook_payload_user_story(self):
        with open("tests/entities/fixtures/user_story_raw.json", encoding="utf-8") as f:
            input_data = json.load(f)
        event = WebhookPayload.model_validate(input_data)
        actual = str(event)
        with open("tests/entities/fixtures/expected_user_story.txt", encoding="utf-8") as f:
            expected = f.read().strip()
        assert actual == expected
