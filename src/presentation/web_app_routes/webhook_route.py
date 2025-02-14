from fastapi import APIRouter
from fastapi.params import Depends
from starlette import status

from src.entities.schemas.project_data.project_types_schemas import ProjectTypeSchema
from src.entities.schemas.webhook_data.webhook_payload_schemas import WebhookPayload
from src.logic.web_app_logic.route_dependency.route_path_validator import (
    validate_event_type,
)

webhook_router = APIRouter()


@webhook_router.post("/{event_type}", status_code=status.HTTP_200_OK)
async def webhook(wh_data: WebhookPayload, event_type: ProjectTypeSchema = Depends(validate_event_type)) -> None:
    """
    Handles incoming webhooks based on the specified event type.

    :param wh_data: Data payload received via the webhook.
    :type wh_data: WebhookPayload
    :param event_type: Type of project for which the webhook is being processed.
    :type event_type: ProjectTypeSchema
    :returns: A success response indicating that the webhook has been received and processed.
    :rtype: None
    """
    pass
