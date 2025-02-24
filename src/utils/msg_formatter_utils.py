import json

from src.core.settings import Configuration
from src.entities.schemas.webhook_data.base_webhook_schemas import Change
from src.entities.schemas.webhook_data.nested_schemas import Milestone, Task, UserStory
from src.entities.schemas.webhook_data.webhook_payload_schemas import WebhookPayload

COMMENT_TEXT_LENGHT = 50


# временная функция, будет заменена на постоянную из пакета утилит работы с языками
def get_translate(key: str) -> str:
    """
    Returns a translated text string.

    :param key: text key in glossary file .yaml
    :type data: str
    :return: text string message
    :rtype: str
    """
    return Configuration.strings.get("formatter_text").get(key)


# TODO функция формирования окончаний файла, нужно привести в соответствие
def get_files_string(count: int) -> str:
    if count == 1:
        return "файл"
    if 1 < count % 10 < 5:
        return f"{count} файла"
    return f"{count} файлов"


def truncate_text_string(text_string: str, lenght: int) -> str:
    """
    Return a truncated string less or equal specified lenght.
    :param text_string: analyzing string
    :type text_string: str
    :param lenght: maximum string lenght
    :type lenght: int
    :return: Text string less or equal 50 chars
    :rtype: str
    """
    return text_string[:lenght] + "..." if len(text_string) > lenght else text_string


def get_parents_name_string(data: Milestone | UserStory | Task, action_key: str) -> str:
    """
    Returns a text string containing the parent objects.

    :param data: data object from payload
    :type data: Milestone, UserStory, Task
    :param action_key: key to determine the preposition in the output string
    :type action_key: str
    :return: Text string message
    :rtype: str
    """
    msg = []
    if hasattr(data, "user_story"):
        msg.append(get_translate(f"message_{action_key}_user_story").format(subject=data.user_story.subject))
    if hasattr(data, "milestone"):
        if not msg:
            msg.append(get_translate(f"message_{action_key}_milestone").format(name=data.milestone.name))
        else:
            msg.append(get_translate("message_of_milestone").format(name=data.milestone.name))
    return ", ".join(msg)


def get_create_delete_message_string(
    action: str,
    username: str,
    obj_type: str,
    obj_data: Milestone | UserStory | Task,
    prefix_message: str,
    timestamp: str,
) -> str:
    """
    Return a text string from the params for create or delete action .
    :param action: action type
    :type action: str
    :param username: action username
    :type username: str
    :param obj_type: object type
    :type obj_type: str
    :param obj_data: object data
    :type obj_data: Milestone | UserStory | Task
    :param prefix_message: prefix string
    :type prefix_message: str
    :param timestamp: action datetime string
    :type timestamp: str
    :return: Text string message
    :rtype: str
    """
    # ключ для правильной работы с предлогами в функции paretns
    action_key = "from" if action == "delete" else "to"
    message_key = f"message_to_{action}_{obj_type}"
    message_body = get_translate(message_key).format(
        username=username,
        obj_name=getattr(obj_data, "subject", getattr(obj_data, "name")),
        parents=get_parents_name_string(obj_data, action_key),
        timestamp=timestamp,
    )
    return prefix_message + message_body


def get_comment_action_message_string(
    username, obj_data: Milestone | UserStory | Task, obj_change: Change, prefix_message: str, timestamp: str
) -> str:
    """
    Return a text string from the params for comments action.
    :param username: action username
    :type username: str
    :param obj_data: object data
    :type obj_data: Milestone | UserStory | Task
    :param obj_change: object, containing comment action data
    :type obj_change: Change
    :param prefix_message: prefix string
    :type prefix_message: str
    :param timestamp: action datetime string
    :type timestamp: str
    :return: Text string message
    :rtype: str
    """
    action = "create"
    # TODO add "edit_comment_date" to Change Object Model
    # if change_data.edit_comment_date:
    #     action = "change"
    if obj_change.delete_comment_date:
        action = "delete"
        action_key = "from"
    action_key = "from" if action == "delete" else "to"
    message_key = f"message_to_{action}_comment"
    message_body = get_translate(message_key).format(
        username=username,
        comment_text=truncate_text_string(obj_change.comment, COMMENT_TEXT_LENGHT),
        parents=get_parents_name_string(obj_data, action_key),
        timestamp=timestamp,
    )
    return prefix_message + message_body


# TODO набросок, доработать


def get_change_object_string(
    obj_data: Milestone | UserStory | Task, obj_type: str, obj_change: Change, PREFIX_MSG: str, SUFFIX_MSG: str
) -> str:
    """
    Return a text string from the params for change events.
    :param obj_data: object data
    :type obj_data: Milestone | UserStory | Task
    :param obj_type: object type
    :type obj_type: str
    :param obj_change: object, containing comment action data
    :type obj_change: Change
    :param PREFIX_MSG: prefix string
    :type PREFIX_MSG: str
    :param SUFFIX_MSG: suffix string
    :type SUFFIX_MSG: str
    :return: Text string message
    :rtype: str
    """
    # Возможны два случая:
    # - внесено одно изменение, ответ вида:
    #     "Пользователь User изменил..... в объекте в "время-дата""
    # - внесено несколько изменений, ответ вида:
    #     "Пользователь User внес следующие изменения в объект в "время дата":
    #         изменение 1,
    #         изменение 2...."
    # готовим list словарей сообщений (в словаре одно сообщение для единичного изменения, второе для множественных)
    # на выходе определяем длину списка и формируем ответ

    changes = []

    # userstory add/remove/replace to/from milestone
    if hasattr(obj_change.diff, "milestone"):
        if not obj_change.diff.milestone.from_:
            changes.append(
                {
                    "single": (f'добавил историю "{obj_data.subject}" к спринту "{obj_change.diff.milestone.to}"'),
                    "multiple": (
                        f'- история "{obj_data.subject}" добавлена к спринту "{obj_change.diff.milestone.to}"'
                    ),
                }
            )
        elif not obj_change.diff.milestone.to:
            changes.append(
                {
                    "single": (f'открепил историю "{obj_data.subject}" от спринта "{obj_change.diff.milestone.from_}"'),
                    "multiple": (
                        f'- история "{obj_data.subject}" откреплена от спринта " {obj_change.diff.milestone.from_}"'
                    ),
                }
            )
        else:
            changes.append(
                {
                    "single": (
                        f'перенес историю "{obj_data.subject}" из спринта "{obj_change.diff.milestone.from_}"'
                        f' в спринт "{obj_change.diff.milestone.to}"'
                    ),
                    "multiple": (
                        f'- история "{obj_data.subject}" перенесена из спринта "{obj_change.diff.milestone.from_}"'
                        f' в спринт "{obj_change.diff.milestone.to}"'
                    ),
                }
            )
    # TODO add actual attributes to Change Object Model
    # if hasattr(payload.change.diff, "sprint_order"):
    #     msg_body = f"изменил сроки окончания спринта \"{obj_data.name}\" проекта \"{obj_data.project.name}\"
    # на {payload.change.diff.sprint_order.to}"

    # change due_date of task
    if hasattr(obj_change.diff, "due_date"):
        changes.append(
            {
                "single": (
                    f'изменил дедлайн задачи "{obj_data.name}" с "{obj_change.diff.due_date.from_}"'
                    f" на {obj_change.diff.due_date.to}"
                ),
                "multiple": (
                    f'- дедлайн задачи "{obj_data.name}" изменен с "{obj_change.diff.due_date.from_}"'
                    f" на {obj_change.diff.due_date.to}"
                ),
            }
        )

    # change due_date of task
    if hasattr(obj_change.diff, "status"):
        changes.append(
            {
                "single": (
                    f'изменил статус задачи "{obj_data.name}" c {obj_change.diff.status.from_}'
                    f" на {obj_change.diff.status.to}"
                ),
                "multiple": (
                    f'- статус задачи "{obj_data.name}" изменен с "{obj_change.diff.status.from_}"'
                    f" на {obj_change.diff.status.to}"
                ),
            }
        )

    # add/change/remove attachments to/from userstory, task
    # TODO
    if hasattr(obj_change.diff, "attachments"):
        # user can add one or more attachments
        if obj_change.diff.attachments.new:
            attachments_names = ", ".join(attachment.filename for attachment in obj_change.diff.attachments.new)
            attachments_count = len(obj_change.diff.attachments.new)

            changes.append(
                {
                    "single": (
                        f'прикрепил {attachments_count} файлов в {obj_type} "{obj_data.name}": {attachments_names}'
                    ),
                    "multiple": (f"- добавлены {attachments_count} файлов: {attachments_names}"),
                }
            )
        # user can change only field "description" only in one attachment
        if obj_change.diff.attachments.changed:
            attachments_name = obj_change.diff.attachments.changed[-1].filename
            desription = obj_change.diff.attachments.changed[-1].changes.description
            changes.append(
                {
                    "single": (
                        f'изменил описание файла {attachments_name} во вложении {obj_type} "{obj_data.name}" на {desription}'
                    ),
                    "multiple": "",
                }
            )

        # user can delete only one attachment
        if obj_change.diff.attachments.deleted:
            attachments_name = obj_change.diff.attachments.deleted[-1].filename
            changes.append(
                {
                    "single": (
                        f'удалил файл {attachments_name} из вложений {obj_type} "{obj_data.name}" на {desription}'
                    ),
                    "multiple": "",
                }
            )
    return None


def get_message_string(payload: WebhookPayload) -> str:
    """
    Return a text string from the instanse WebhookPayload object data.

    :param payload: payload from webhook
    :type payload: WebhookPayload
    :return: Text string message
    :rtype: str
    """
    prefix_msg = get_translate("message_prefix_project_name").format(project_name=payload.data.project.name)
    timestamp = payload.date.strftime("%H:%M %d.%m.%Y")

    # message for "create" or "delete" action
    if payload.action in ["create", "delete"]:
        return get_create_delete_message_string(
            payload.action, payload.by.full_name, payload.type, payload.data, prefix_msg, timestamp
        )

    # message for "test" action
    if payload.action == "test":
        pass

    # messages for "change" action
    if payload.action == "change":
        # comment create, edit, delete, action
        if hasattr(payload.change, "comment") and payload.change.comment:
            return get_comment_action_message_string(
                payload.by.full_name, payload.data, payload.change, prefix_msg, timestamp
            )
        # not comment changes:
        return get_change_object_string(payload.data, payload.type, payload.change, prefix_msg, timestamp)

    return "No template was found to process the event that occurred."


# test block
# to delete
# -----------------
with open("tests/entities/fixtures/milestone_raw.json", encoding="utf-8") as f:
    input_data = json.load(f)
event = WebhookPayload.model_validate(input_data)
print(get_message_string(event))
# -----------------
