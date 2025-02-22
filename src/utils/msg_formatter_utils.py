import json

from src.core.settings import Configuration
from src.entities.schemas.webhook_data.nested_schemas import Milestone, Task, UserStory
from src.entities.schemas.webhook_data.webhook_payload_schemas import WebhookPayload


def get_translate(key: str) -> str:
    """
    Returns a translated text string.

    :param key: text key in glossary file .yaml
    :type data: str
    :return: text string message
    :rtype: str
    """
    return Configuration.strings.get("formatter_text").get(key)


def get_parents_name_string(data: Milestone | UserStory | Task) -> str:
    """
    Returns a text string containing the parent objects.

    :param data: data object from payload
    :type data: Milestone, UserStory, Task
    :return: Text string message
    :rtype: str
    """
    msg = []
    if hasattr(data, "user_story"):
        msg.append(get_translate("in_user_story").format(SUBJECT=data.user_story.subject))
    if hasattr(data, "milestone"):
        if not msg:
            msg.append(get_translate("in_milestone").format(NAME=data.milestone.name))
        else:
            msg.append(get_translate("of_milestone").format(NAME=data.milestone.name))
    if not msg:
        msg.append(get_translate("in_project").format(NAME=data.project.name))
    else:
        msg.append(get_translate("of_project").format(NAME=data.project.name))
    return ", ".join(msg)


def get_create_delete_body_string(action: str, obj_type: str, data: Milestone | UserStory | Task) -> str:
    """
    Return a text string from the params.
    :param action: action type
    :type payload: str
    :param payload: object type
    :type payload: str
    :param data: data object from payload
    :type data: Milestone, UserStory, Task
    :return: Text string message
    :rtype: str
    """
    ACTION = get_translate(action)
    OBJ_TYPE = get_translate(obj_type)
    PARENTS = get_parents_name_string(data)
    return f"{ACTION} {OBJ_TYPE} {PARENTS}"


def get_message_string(payload: WebhookPayload) -> str:
    """
    Return a text string from the instanse WebhookPayload object data.

    :param payload: payload from webhook
    :type payload: WebhookPayload
    :return: Text string message
    :rtype: str
    """

    action = payload.action
    obj_type = payload.type
    obj_data = payload.data

    PREFIX_MSG = get_translate("username_prefix").format(USERNAME=payload.by.full_name)
    SUFFIX_MSG = get_translate("timestamp_suffix").format(TIMESTAMP=payload.date.strftime("%H:%M %d.%m.%Y"))

    # message for "create" or "delete" action
    if action in ["create", "delete"]:
        obj_type = "new_" + obj_type
        return f"{PREFIX_MSG} {get_create_delete_body_string(action, obj_type, obj_data)} {SUFFIX_MSG}"

    # message for "test" action
    if action == "test":
        pass

    # messages for "change" action
    # пользователь может внести сразу несколько изменений
    # сначала соберем список фрагментов текстов, а потом добавим префикс, если
    # изменений было несколько

    # messages for "comment" action
    # if payload.change.comment:
    #     # события с комментами - создан, удален, изменен
    #     pass

    # if hasattr(payload.change.diff, "milestone"):
    #     msg_body = f"добавил историю \"{obj_data.subject}\" к спринту \"{payload.change.diff.milestone.to}\""

    # if hasattr(payload.change.diff, "sprint_order"):
    #     msg_body = f"изменил сроки окончания спринта \"{obj_data.name}\" проекта \"{obj_data.project.name}\"
    # на {payload.change.diff.sprint_order.to}"

    # if hasattr(payload.change.diff, "due_date"):
    #     msg_body = f"установил дедлайн задачи \"{obj_data.name}\" !!!!истории спринта проекта
    # \"{obj_data.project.name}\" на {payload.change.diff.due_date.to}"

    # if hasattr(payload.change.diff, "status"):
    #     msg_body = f"изменил статус {obj_type} \"{obj_data.name}\" !!!!истории спринта проекта
    # \"{obj_data.project.name}\" c {payload.change.diff.status.from_} на {payload.change.diff.status.to}"

    # if hasattr(payload.change.diff, "attachments"):
    #     # перебираем три варианта: новые, изменены, удалены
    #     if payload.change.diff.attachments.new:
    #         attachments_names = ", ".join(
    #             (attachment.name for attachment in payload.change.diff.attachments.new))
    #         return f'{username} add new attachments "{attachments_names}" at {timestamp}'
    #     if payload.change.diff.attachments.changed:
    #         attachments_names = ", ".join(
    #             (attachment.name for attachment in payload.change.diff.attachments.new))
    #         return f'{username} change attachments "{attachments_names}" at {timestamp}'
    #     if payload.change.diff.attachments.deleted:
    #         attachments_names = ", ".join(
    #             (attachment.name for attachment in payload.change.diff.attachments.new))
    #         return f'{username} delete attachments "{attachments_names}" at {timestamp}'
    #     pass

    return "No template was found to process the event that occurred."


# этот блок будет удален
# -----------------
with open("tests/entities/fixtures/milestone_raw.json", encoding="utf-8") as f:
    input_data = json.load(f)
event = WebhookPayload.model_validate(input_data)
print(get_message_string(event))
# -----------------
