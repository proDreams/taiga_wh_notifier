import asyncio
from datetime import datetime

from src.core.settings import get_logger, get_settings
from src.entities.enums.event_enums import EventActionEnum
from src.entities.schemas.project_data.project_schemas import ProjectSchema
from src.entities.schemas.webhook_data.webhook_payload_schemas import WebhookPayload
from src.infrastructure.broker.redis_dependency import RedisSessionDependency
from src.infrastructure.broker.redis_manager import RedisManager
from src.utils.aggregate_webhooks_utils import aggregate_wh_list
from src.utils.msg_formatter_utils import get_message
from src.utils.send_message_utils import send_message

logger = get_logger(name=__name__)


class WebhookService:
    """
    Service class for managing webhook operations
    """

    def __init__(self) -> None:
        """
        Initializes the WebhookService instance.

        This constructor sets up the Redis connection by creating an instance
        of RedisManager.
        """
        self._redis_manager = RedisManager(redis_dep=RedisSessionDependency())

    async def process_wh_data(self, wh_data: WebhookPayload, project: ProjectSchema) -> None:
        """
        Processes incoming webhook data and queues it for further handling or aggregation.

        :param wh_data: The webhook payload.
        :type wh_data: WebhookPayload.
        :param project: The project schema to associate with the webhook data for further processing.
        :type project: ProjectSchema.
        """
        redis_key = self.__get_redis_key(wh_data)

        if wh_data.action == EventActionEnum.CREATE or wh_data.action == EventActionEnum.TEST:
            logger.info('Received webhook has action "Create" or "Test". Passed for processing without aggregation.')
            asyncio.create_task(self.proceed_wh_data(wh_data=wh_data, project=project, params={}))
            return

        # to del after aggregator proceed comment and attachments
        # ----------------------
        if getattr(wh_data, "change", None) and (wh_data.change.comment or wh_data.change.diff.attachments):
            logger.info(
                "Received webhook has comment or attachments change. Passed for processing without aggregation."
            )
            asyncio.create_task(self.proceed_wh_data(wh_data=wh_data, project=project, params={}))
            return
        # ----------------------

        logger.info(f'Received webhook has been submitted for aggregation queuing type:id="{redis_key}"')
        is_exists_queue = await self._redis_manager.add_wh_to_sorted_set(
            key=redis_key,
            value=wh_data.model_dump_json(by_alias=True),
            timestamp=int(datetime.timestamp(wh_data.date)),
        )
        if not is_exists_queue:
            logger.info(
                f'A new queue has been created: type:id="{redis_key}". '
                "Creating a delayed task for aggregation and processing of webhooks."
            )
            asyncio.create_task(self._aggregation_task(redis_key=redis_key, project=project))

    @staticmethod
    def __get_redis_key(wh_data: WebhookPayload) -> str | None:
        """
        Generates a Redis key based on the webhook data.

        :param wh_data: The webhook payload.
        :type wh_data: WebhookPayload.
        :return: Generated Redis key or None (for Test Webhook Payload).
        :rtype: str | None
        """
        return f"{wh_data.type.value}:{wh_data.data.id}" if wh_data.action != EventActionEnum.TEST else None

    async def _aggregation_task(self, redis_key: str, project: ProjectSchema) -> None:
        """
        Processes a new webhook aggregation task.

        :param redis_key: The Redis key used for storing and retrieving aggregated webhooks.
        :type redis_key: str.
        """
        await asyncio.sleep(get_settings().AGGREGATION_DELAY_SECONDS)
        wh_data_sorted_list = await self._redis_manager.get_wh_sorted_list(key=redis_key)
        if len(wh_data_sorted_list) == 0:
            logger.debug(
                f'The obtained list of webhooks for the task task for type:id="{redis_key}" is empty. Task aborted.'
            )
            return

        aggregated_wh, params = aggregate_wh_list(wh_data_sorted_list)

        if aggregated_wh.action == EventActionEnum.CHANGE and "no_aggregate_changes" in params:
            logger.debug("The aggregated webhook does not contain changes. Task aborted.")
            return

        logger.info("The aggregated webhook has been passed for processing.")
        await self.proceed_wh_data(wh_data=aggregated_wh, project=project, params=params)

    @staticmethod
    async def proceed_wh_data(
        wh_data: WebhookPayload,
        project: ProjectSchema,
        params: dict[str, dict],
    ) -> ProjectSchema | None:
        """
        Processes webhook data by generating a message and sending it to a chat.

        :param wh_data: The webhook payload.
        :type wh_data: WebhookPayload.
        :param project: The project schema to associate with the webhook data for further processing.
        :type project: ProjectSchema.
        :param params: Additional parameters for message generation.
        :type params: dict[str, dict].
        """
        instance = project.instances[0]

        text, attachments = get_message(payload=wh_data, lang=instance.language, params=params)

        await send_message(
            chat_id=instance.chat_id,
            text=text,
            message_thread_id=instance.thread_id,
            link_preview_options=None,
            disable_web_page_preview=True,
        )


def get_webhook_service():
    """Return WebhookService instance."""
    return WebhookService()
