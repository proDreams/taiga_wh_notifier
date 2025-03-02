import json

from src.entities.schemas.webhook_data.base_webhook_schemas import DiffAttachments
from src.entities.schemas.webhook_data.nested_schemas import (
    Milestone,
    Project,
    Task,
    UserStory,
)
from src.entities.schemas.webhook_data.webhook_payload_schemas import (
    Change,
    WebhookPayload,
)
from src.utils.text_utils import localize_text_to_message

# datetime format
TIMESTAMP_FORMAT = "%H:%M %d.%m.%Y"
# output fields
MESSAGE_SCHEMA = {
    "epic": {
        "create": (["action", "object_of_action"], ["parents"], ["timestamp", "by_fullname", "assigned_to"], ["tags"]),
        "change": (
            ["action", "object_of_action"],
            ["parents"],
            ["timestamp", "by_fullname", "assigned_to"],
            ["change"],
            ["tags"],
        ),
        "delete": (["action", "object_of_action"], ["parents"], ["timestamp", "by_fullname", "assigned_to"], ["tags"]),
    },
    "milestone": {
        "create": (["action", "object_of_action"], ["parents"], ["timestamp", "by_fullname"], ["estimated_finish"]),
        "change": (
            ["action", "object_of_action"],
            ["parents"],
            ["timestamp", "by_fullname"],
            ["estimated_finish"],
            ["change"],
        ),
        "delete": (
            ["action", "object_of_action"],
            ["parents"],
            ["timestamp", "by_fullname"],
        ),
    },
    "userstory": {
        "create": (
            ["action", "object_of_action"],
            ["parents"],
            ["timestamp", "by_fullname", "assigned_to"],
            ["tags", "status"],
            ["points"],
            ["client_requirement", "team_requirement"],
            ["is_blocked"],
        ),
        "change": (
            ["action", "object_of_action"],
            ["parents"],
            ["timestamp", "by_fullname", "assigned_to"],
            ["change"],
            ["tags"],
        ),
        "delete": (["action", "object_of_action"], ["parents"], ["timestamp", "by_fullname", "assigned_to"], ["tags"]),
    },
    "task": {
        "create": (
            ["action", "object_of_action"],
            ["parents"],
            ["timestamp", "by_fullname", "assigned_to"],
            ["status", "due_date"],
            ["tags", "is_iocaine"],
            ["is_blocked"],
        ),
        "change": (
            ["action", "object_of_action"],
            ["parents"],
            ["timestamp", "by_fullname", "assigned_to"],
            ["change"],
            ["tags", "is_iocaine"],
        ),
        "delete": (
            ["action", "object_of_action"],
            ["parents"],
            ["timestamp", "by_fullname", "assigned_to"],
            ["tags", "is_iocaine"],
        ),
    },
    "issue": {
        "create": (
            ["action", "object_of_action"],
            ["parents"],
            ["timestamp", "by_fullname", "assigned_to"],
            ["tags", "due_date"],
            ["type", "priority", "severity"],
            ["is_blocked"],
        ),
        "change": (
            ["action", "object_of_action"],
            ["parents"],
            ["timestamp", "by_fullname", "assigned_to"],
            ["change"],
            ["tags"],
            ["is_blocked"],
        ),
        "delete": (
            ["action", "object_of_action"],
            ["parents"],
            ["timestamp", "by_fullname", "assigned_to"],
            ["tags"],
            ["is_blocked"],
        ),
    },
    "wikipage": {
        "create": (["action", "object_of_action"], ["parents"], ["timestamp", "by_fullname"]),
        "change": (
            ["action", "object_of_action"],
            ["parents"],
            ["timestamp", "by_fullname"],
            ["change"],
        ),
        "delete": (
            ["action", "object_of_action"],
            ["parents"],
            ["timestamp", "by_fullname", "assigned_to"],
        ),
    },
    "test": {"create": (["action", "object_of_action"], ["parents"], ["timestamp", "by_fullname", "assigned_to"])},
}

# временная функция, будет заменена на постоянную из пакета утилит работы с языками


def get_yaml_string(key: str, **kwargs) -> str:
    return localize_text_to_message(key, "ru", **kwargs)


def get_object_name(data: Milestone | UserStory | Task | Project) -> str:
    """
    Return a object name from "subject" or "name" field.
    :param data: data object from payload
    :type data: Milestone, UserStory, Task
    :return: object name or ""
    :rtype: str
    """
    if hasattr(data, "subject"):
        return data.subject
    if hasattr(data, "name"):
        return data.name
    return ""


def get_object_with_url(payload: WebhookPayload) -> str:
    """
    Return a string from template, contained type, name (if is), url of object.
    :param payload: payload from webhook
    :type payload: WebhookPayload
    :return: string from template, contained type, name (if is), url of object
    :rtype: str
    """

    # if object is wiki - it hasn't name or subject field
    if payload.type == "wikipage":
        # TODO проверить правильность работы блока
        return get_yaml_string(
            "object_action_url_wiki_string", obj_type=get_yaml_string(payload.type), permalink=payload.data.permalink
        )
    return get_yaml_string(
        "object_action_url_string",
        obj_type=get_yaml_string(payload.type),
        obj_name=get_object_name(payload.data),
        permalink=payload.data.permalink,
    )


def get_parents(data: Milestone | UserStory | Task) -> dict:
    """
    Return a string, contained parents of objects.

    :param data: data object from payload
    :type data: Milestone, UserStory, Task
    :return: string, contained parents of objects
    :rtype: str
    """
    parents_list = []
    instances = ("project", "epic", "milestone", "userstory")
    for instance in instances:
        if hasattr(data, instance):
            parents_list.append(
                get_yaml_string(
                    "object_with_name_string",
                    obj_type=get_yaml_string(instance),
                    obj_name=get_object_name(getattr(data, instance)),
                )
            )
    return "".join(parents_list)


def get_assigned_to(data: Milestone | UserStory | Task) -> str:
    """
    Return string, contained "assigned_to" info

    :param data: data object from payload
    :type data: Milestone, UserStory, Task
    :return: string message
    :rtype: str
    """
    assigned_suffix = ""
    # for webhook with "assigned_users" field check possible more than 1 assigneds
    if hasattr(data, "assigned_users"):
        count_assigneds = len(data.assigned_users)
        if count_assigneds > 1:
            assigned_suffix = f" + {count_assigneds - 1}"
    return get_yaml_string("assigned_to_string", assigned=(data.assigned_to + assigned_suffix))


def get_points_string(data: Milestone | UserStory | Task) -> str:
    if hasattr(data, "points"):
        total_scores = 0
        points = []
        for point in data.points:
            if point.value:
                total_scores += point.value
                points.append(f"{point.role}: {point.value}")
        if points:
            return get_yaml_string("points_string", points=f"{", ".join(points)}", total_scores=total_scores)
    return ""


def get_comment_string(change: Change) -> str:
    """
    Return string, contained "comments action" info

    :param change: change object from payload
    :type change: Change
    :return: string message
    :rtype: str
    """
    action = "create"
    if change.delete_comment_date:
        action = "delete"
    # TODO add edit_comment_date field into model
    # if change.edit_comment_date:
    #     action = "change"
    # TODO truncate comment text if need?
    return get_yaml_string("comment_change_string", action=get_yaml_string(action), comment_text=change.comment)


def get_attachment_string(attachments: DiffAttachments) -> str:
    """
    Return string, contained "attachments action" info

    :param change: attachmeents object from change
    :type change: DiffAttachments
    :return: string message
    :rtype: str
    """
    # if change in one attachement
    # WebHook is not contained filename or another info about attachment
    if attachments.changed:
        return get_yaml_string("attachments_change_string")

    # if new atachments or delete one attachement
    attr_name = "new"
    action = "create"
    if attachments.deleted:
        attr_name = "deleted"
        action = "delete"
    filenames = ", ".join([file_object.filename for file_object in getattr(attachments, attr_name)])
    return get_yaml_string("attachments_string", action=get_yaml_string(action), filenames=filenames)


def get_from_to_key(change: Change, key: str) -> str:
    if not getattr(change.diff, key).from_:
        return "from_none"
    if not getattr(change.diff, key).to:
        return "to_none"
    return "from_to"


def get_changes(change: Change) -> str:
    """
    Return strings, contained changes info strings

    :param change: change object from payload
    :type change: Change
    :return: string message
    :rtype: str
    """
    # comments action in change
    if change.comment:
        return get_comment_string(change)

    # attachments action in change
    if hasattr(change.diff, "attachments") and change.diff.attachments:
        return get_attachment_string(change.diff.attachments)

    # all other types of change actions can contained more than one in WebHook
    changes_list = []

    # TODO calculate points
    if hasattr(change.diff, "points"):
        pass

    changes_attr = (
        "name",
        "subject",
        "status",
        "due_date",
        "milestone",
        "team_requirement",
        "client_requirement",
        "description",
        "assigned_to",
        "is_blocked",
        "is_iocaine",
        "type",
        "priority",
        "severity",
    )
    to_translate_fields = ("status", "type", "priority", "severity")

    for attr in changes_attr:
        if hasattr(change.diff, attr):
            from_to_key = get_from_to_key(change.diff, attr)
            from_ = (getattr(change.diff, attr).from_,)
            to = getattr(change.diff, attr).to
            # translate field value if need
            if attr in to_translate_fields:
                from_ = get_yaml_string(from_)
                to = get_yaml_string(to)
            changes_list.append(get_yaml_string(f"change_{attr}_{from_to_key}_string", from_=from_, to=to))

    return "\n".join(changes_list)


def get_strings(payload: WebhookPayload, field: str) -> str:
    """
    Return a parsed string from the instanse WebhookPayload object data.

    :param payload: payload from webhook
    :type payload: WebhookPayload
    :param field: parsing field
    :type field: str
    :return: parsed string
    :rtype: str
    """
    match field:
        case "action":
            return get_yaml_string("action_string", action=get_yaml_string(payload.action))

        case "object_of_action":
            return get_object_with_url(payload)

        case "parents":
            return get_parents(payload.data)

        case "timestamp":
            return get_yaml_string("action_time_string", timestamp=payload.date.strftime(TIMESTAMP_FORMAT))

        case "by_fullname":
            return get_yaml_string("action_author_string", author=payload.by.full_name)

        # # TODO разобраться с assgined_to - есть инфа об 1 отв + число из списка
        # # TODO для проверки работы функции - нужно внести корректировки в модель
        # case "assigned_to", payload.data.assigned_to:
        #     return get_assigned_to(payload.data)

        case "change":
            return get_yaml_string("change_string", change=get_changes(payload.change))

        case "status", payload.data.status:
            return get_yaml_string(
                "status_string", status=get_yaml_string(f"status_{payload.data.status.name.lower()}")
            )

        case "due_date", payload.data.due_date:
            return get_yaml_string("due_date_string", due_date=payload.data.due_date)

        case "estimated_finish", payload.data.estimated_finish:
            return get_yaml_string("due_date_string", due_date=payload.data.estimated_finish)

        case "tags", payload.data.tags:
            return get_yaml_string("tags_string", tags=", ".join(payload.data.tags))

        # # TODO для проверки нужна модель Task
        # case "is_iocaine":
        #     return get_yaml_string("is_iocaine_string", is_iocaine=get_yaml_string(payload.data.is_iocaine))

        # # TODO поля для issue отсутствуют в модели
        # # ----------------------------------------------------
        case "type", payload.data.type:
            return get_yaml_string("issue_type_string", issue_type=payload.data.type.lower())

        case "priority", payload.data.priority:
            return get_yaml_string("issue_priority_string", priority=payload.data.priority.lower())

        case "severity", payload.data.severity:
            return get_yaml_string("issue_severity_string", severity=payload.data.severity.lower())
        # # ----------------------------------------------------

        case "points":
            return get_points_string(payload.data)

        case "client_requirement", payload.data.client_requirement:
            return get_yaml_string("client_requirement_string")

        case "team_requirement", payload.data.team_requirement:
            return get_yaml_string("team_requirement_string")

    return ""


def get_message(payload: WebhookPayload) -> str:
    """
    Return a text string from the instanse WebhookPayload object data.

    :param payload: payload from webhook
    :type payload: WebhookPayload
    :return: Text string message
    :rtype: str
    """
    output_fields = MESSAGE_SCHEMA.get(payload.type).get(payload.action)

    # output_fields = MESSAGE_SCHEMA.get("test").get("create")

    if not output_fields:
        # TODO вызвать исключение или вернуть текст с ошибкой
        pass

    output_message = []
    for text_block in output_fields:
        output_block = []
        for field in text_block:
            field_string = get_strings(payload, field)
            if field_string:
                output_block.append(field_string)
        if output_block:
            output_message.append("".join(output_block))
    return "\n".join(output_message)


# test block
# to delete
# -----------------
with open("tests/entities/fixtures/milestone_raw.json", encoding="utf-8") as f:
    input_data = json.load(f)
event = WebhookPayload.model_validate(input_data)
print(get_message(event))
# -----------------
