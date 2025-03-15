from src.entities.schemas.project_data.project_schemas import ProjectSchema
from src.entities.schemas.webhook_data.webhook_payload_schemas import WebhookPayload
from src.utils.msg_formatter_utils import get_message
from src.utils.send_message_utils import send_message


class WebhookService:
    @staticmethod
    async def process_wh_data(
        wh_data: WebhookPayload,
        project: ProjectSchema,
    ) -> ProjectSchema | None:
        instance = project.instances[0]
        text, attachments = get_message(payload=wh_data, lang=instance.language)

        await send_message(
            chat_id=instance.chat_id,
            text=text,
            message_thread_id=instance.thread_id,
            link_preview_options=None,
            disable_web_page_preview=True,
        )
