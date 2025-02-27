import json

from src.core.settings import Configuration
from src.entities.schemas.webhook_data.base_webhook_schemas import Change
from src.entities.schemas.webhook_data.nested_schemas import Milestone, Task, UserStory
from src.entities.schemas.webhook_data.webhook_payload_schemas import WebhookPayload

COMMENT_TEXT_LENGHT = 50


# временная функция, будет заменена на постоянную из пакета утилит работы с языками
def get_translate(key: str) -> str:
    """
    Return a translated text string.

    :param key: text key in glossary file .yaml
    :type data: str
    :return: text string message
    :rtype: str
    """
    return Configuration.strings.get("formatter_text").get(key)


# TODO функция формирования окончаний файла, нужно привести в соответствие
def get_count_files_string(count: int) -> str:
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
    Return a text string containing the parent objects.

    :param data: data object from payload
    :type data: Milestone, UserStory, Task
    :param action_key: key to determine the preposition in the output string
    :type action_key: str
    :return: Text string message
    :rtype: str
    """
    msg = []
    if hasattr(data, "user_story"):
        msg.append(get_translate(f"message_{action_key}_userstory").format(obj_name=data.user_story.subject))
    if hasattr(data, "milestone"):
        if not msg:
            msg.append(get_translate(f"message_{action_key}_milestone").format(obj_name=data.milestone.name))
        else:
            msg.append(get_translate("message_of_milestone").format(obj_name=data.milestone.name))
    return ", ".join(msg)


def get_object_with_name_string(obj_data: Milestone | UserStory | Task, obj_type: str, action_key: str) -> str:
    return get_translate(f"message_{action_key}_{obj_type}").format(
        obj_name=getattr(obj_data, "subject", getattr(obj_data, "name", None)),
    )


def get_create_delete_message_string(
    action: str,
    username: str,
    obj_type: str,
    obj_data: Milestone | UserStory | Task,
    prefix_message: str,
    timestamp: str,
) -> str:
    """
    Return a text string from the params for create or delete action.

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
        obj_name=getattr(obj_data, "subject", getattr(obj_data, "name", None)),
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


def get_change_object_string(
    username: str,
    obj_data: Milestone | UserStory | Task,
    obj_type: str,
    obj_change: Change,
    prefix_message: str,
    timestamp: str,
) -> str:
    """
    Return a text string from the params for change events.

    :param username: action username
    :type username: str
    :param obj_data: object data
    :type obj_data: Milestone | UserStory | Task
    :param obj_type: object type
    :type obj_type: str
    :param obj_change: object, containing comment action data
    :type obj_change: Change
    :param prefix_message: prefix string
    :type prefix_message: str
    :param timestamp: action datetime string
    :type timestamp: str
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

    entity = get_translate(f"message_of_{obj_type}").format(
        obj_name=getattr(obj_data, "subject", getattr(obj_data, "name", None)),
    )
    parents = get_parents_name_string(obj_data, "of")
    changes = []

    # userstory add/remove/replace to/from milestone
    # TODO при добавлении к спринту появляется параметр sprint_order. Нужно разобраться
    if hasattr(obj_change.diff, "milestone") and obj_change.diff.milestone:
        if not obj_change.diff.milestone.from_:
            from_to_key = "from_none"
        elif not obj_change.diff.milestone.to:
            from_to_key = "to_none"
        else:
            from_to_key = "from_to"
        changes.append(
            {
                "single": get_translate(f"message_to_change_milestone_{from_to_key}").format(
                    username=username,
                    user_story_name=obj_data.subject,
                    milestone_from=obj_change.diff.milestone.from_,
                    milestone_to=obj_change.diff.milestone.to,
                    timestamp=timestamp,
                ),
                "multiple": "",
            }
        )

    # change due_date of userstory/task
    if hasattr(obj_change.diff, "due_date") and obj_change.diff.due_date:
        if not obj_change.diff.due_date.from_:
            from_to_key = "from_none"
        elif not obj_change.diff.due_date.to:
            from_to_key = "to_none"
        else:
            from_to_key = "from_to"
        changes.append(
            {
                count_changes_key: get_translate(
                    f"message_to_change_due_date_{from_to_key}_{count_changes_key}"
                ).format(
                    username=username,
                    entity=entity,
                    parents=parents,
                    from_=obj_change.diff.due_date.from_,
                    to=obj_change.diff.due_date.to,
                    timestamp=timestamp,
                )
                for count_changes_key in ["single", "multiple"]
            }
        )

    # change status of userstory/task
    if hasattr(obj_change.diff, "status") and obj_change.diff.status:
        status_from = get_translate(f"message_to_status_{"_".join(obj_change.diff.status.from_.lower().split())}")
        status_to = get_translate(f"message_to_status_{"_".join(obj_change.diff.status.to.lower().split())}")
        changes.append(
            {
                count_changes_key: get_translate(f"message_to_change_status_{count_changes_key}").format(
                    username=username,
                    entity=entity,
                    parents=parents,
                    from_=status_from,
                    to=status_to,
                    timestamp=timestamp,
                )
                for count_changes_key in ["single", "multiple"]
            }
        )

    # TODO add actual attributes to Change Object Model
    # if hasattr(payload.change.diff, "sprint_order"):
    #     msg_body = f"изменил сроки окончания спринта \"{obj_data.name}\" проекта \"{obj_data.project.name}\"
    # на {payload.change.diff.sprint_order.to}"

    # add/change/remove attachments to/from userstory, task
    if hasattr(obj_change.diff, "attachments") and obj_change.diff.attachments:
        # user can add one or more attachments
        if obj_change.diff.attachments.new:
            filenames = "\n".join(f"- {attachment.filename}" for attachment in obj_change.diff.attachments.new)
            changes.append(
                {
                    "single": get_translate("message_to_add_attachments").format(
                        username=username,
                        count_files=get_count_files_string(len(obj_change.diff.attachments.new)),
                        obj_with_name=get_object_with_name_string(obj_data, obj_type, "to"),
                        parents=parents,
                        timestamp=timestamp,
                        filenames=filenames,
                    ),
                    "multiple": "",
                }
            )

        # TODO add fields to a Change Object Model
        # # user can change only field "description" only in one attachment
        # if obj_change.diff.attachments.changed:
        #     kwargs = {
        #         "username": username,
        #         "filename": obj_change.diff.attachments.changed[0].filename,
        #         "obj_with_name": get_object_with_name_string(obj_data, obj_type, "at"),
        #         "parents": parents,
        #         "timestamp": timestamp
        #     }
        #     if hasattr(obj_change.diff.attachments.changed[0].changes, "description"):
        #         message_key = "description"
        #         kwargs["description"] = obj_change.diff.attachments.changed[0].changes.description
        #     if hasattr(obj_change.diff.attachments.changed[0].changes, "is_deprecated"):
        #         if obj_change.diff.attachments.changed[0].changes.is_deprecated:
        #             message_key = "is_deprecated"
        #         else:
        #             message_key = "is_not_deprecated"
        #     changes.append(
        #         {
        #             "single": get_translate(f"message_to_change_attachments_{message_key}").format(**kwargs),
        #             "multiple": ""
        #         }
        #     )

        if obj_change.diff.attachments.deleted:
            changes.append(
                {
                    "single": get_translate("message_to_delete_attachments").format(
                        username=username,
                        filename=obj_change.diff.attachments.deleted[0].filename,
                        obj_with_name=get_object_with_name_string(obj_data, obj_type, "from"),
                        parents=parents,
                        timestamp=timestamp,
                    ),
                    "multiple": "",
                }
            )

    count_key = "single"
    if len(changes) > 1:
        prefix_message += get_translate("message_add_prefix_for_multiple_changes").format(
            username=username, entity=entity, parents=parents, timestamp=timestamp
        )
        count_key = "multiple"
    message_body = "\n".join(action[count_key] for action in changes)
    return prefix_message + message_body


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
        return get_change_object_string(
            payload.by.full_name, payload.data, payload.type, payload.change, prefix_msg, timestamp
        )

    return "No template was found to process the event that occurred."


# test block
# to delete
# -----------------
with open("tests/entities/fixtures/test.json", encoding="utf-8") as f:
    input_data = json.load(f)
event = WebhookPayload.model_validate(input_data)
print(get_message_string(event))
# -----------------
