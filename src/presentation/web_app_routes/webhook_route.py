from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from starlette import status

from src.entities.schemas.project_data.project_schemas import ProjectSchema
from src.entities.schemas.webhook_data.webhook_payload_schemas import WebhookPayload
from src.logic.services.webhook_service import WebhookService
from src.logic.web_app_logic.route_dependency.route_path_validator import (
    validate_instance,
)

webhook_router = APIRouter()


@webhook_router.post("/{instance}", status_code=status.HTTP_204_NO_CONTENT)
async def webhook(wh_data: WebhookPayload, instance: ProjectSchema = Depends(validate_instance)) -> None:
    """
    Handles incoming webhooks based on the specified event type.

    :param wh_data: Data payload received via the webhook.
    :type wh_data: WebhookPayload
    :param instance: Project for which the webhook is being processed.
    :type instance: ProjectSchema
    :returns: A success response indicating that the webhook has been received and processed.
    :rtype: None
    """
    if wh_data.type in instance.instances[0].fat:
        await WebhookService.process_wh_data(wh_data=wh_data, project=instance)
        return

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Instance {instance} not found")
