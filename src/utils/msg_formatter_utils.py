import json

from src.core.settings import get_settings, get_strings
from src.entities.enums.event_enums import EventChangeEnum
from src.entities.schemas.webhook_data.diff_webhook_schemas import (
    Diff,
    DiffAttachments,
    Points,
)
from src.entities.schemas.webhook_data.nested_schemas import (
    Epic,
    Issue,
    Milestone,
    Project,
    Task,
    UserStory,
    Wiki,
)
from src.entities.schemas.webhook_data.webhook_payload_schemas import (
    Change,
    WebhookPayload,
)
from src.utils.text_utils import format_text_with_kwargs


def get_yaml_string(text_in_yaml: str, lang: str = "ru", **kwargs) -> str:
    return format_text_with_kwargs(
        text_in_yaml=get_strings().get("webhook_notifications").get(lang).get(text_in_yaml), **kwargs
    )


def get_truncated_string(text: str) -> str:
    maximum_text_lenght = get_settings().TRUNCATED_STRING_LENGHT
    if len(text) > maximum_text_lenght:
        # TODO add html_tags clear method
        return text[:maximum_text_lenght] + "..."
    return text


def get_object_name(data: Milestone | Epic | UserStory | Task | Issue | Wiki) -> str:
    """
    Return a object name from "name" (for Milestone) or "subject" (for all other objects) field or None (for wiki).
    :param data: data object from payload
    :type data: Milestone, Epic, UserStory, Task, Issue, Wiki
    :return: object name or empty string
    :rtype: str | None
    """
    if hasattr(data, "subject"):
        return data.subject
    if hasattr(data, "name"):
        return data.name
    return ""


def get_object_with_url(payload: WebhookPayload) -> str:
    """
    Return a string from template, contained type, name (if defined), url of object.
    :param payload: payload from webhook
    :type payload: WebhookPayload
    :return: string from template
    :rtype: str
    """
    kwargs = {"obj_type": get_yaml_string(payload.type), "permalink": payload.data.permalink}
    # if object is wiki - it hasn't "name" or "subject" field
    if payload.type == "wikipage":
        return get_yaml_string("object_action_url_wiki_string", **kwargs)

    # otherwise, add object_name field
    kwargs["obj_name"] = get_object_name(payload.data)
    return get_yaml_string("object_action_url_string", **kwargs)


def get_parents(data: Milestone | Epic | UserStory | Task | Issue | Wiki) -> str:
    """
    Return a string, contained parents of objects.

    :param data: data object from payload
    :type data: Milestone, Epic, UserStory, Task, Issue, Wiki
    :return: string, contained parents of objects
    :rtype: str
    """
    parents_list = []
    instances = ("project", "epic", "milestone", "userstory")
    for instance in instances:
        if hasattr(data, instance) and getattr(data, instance):
            parents_list.append(
                get_yaml_string(
                    "object_with_name_string",
                    obj_type=get_yaml_string(instance),
                    obj_name=get_object_name(getattr(data, instance)),
                )
            )
    return "".join(parents_list)


def get_assigned_to(data: Milestone | Epic | UserStory | Task | Project | Issue | Wiki) -> str:
    """
    Return string, contained "assigned_to" info

    :param data: data object from payload
    :type data: Milestone, Epic, UserStory, Task, Issue, Wiki
    :return: string, contained "assigned_to" info
    :rtype: str
    """
    assigned_suffix = ""
    # if object "assigned to" more than one user, add information about the number of users
    if hasattr(data, "assigned_users") and data.assigned_users:
        count_assigneds = len(data.assigned_users)
        if count_assigneds > 1:
            assigned_suffix = f" + {count_assigneds - 1}"
    return get_yaml_string("assigned_to_string", assigned=(data.assigned_to.full_name + assigned_suffix))


def get_points_string(data: Milestone | Epic | UserStory | Task | Project | Wiki | Issue) -> str:
    """
    Return string, contained points information and calculated total points

    :param data: data object from payload
    :type data: Milestone, Epic, UserStory, Task, Issue, Wiki
    :return: string, contained points information
    :rtype: str
    """
    total_points = 0
    points = []
    for point in data.points:
        if point.value:
            total_points += point.value
            points.append(f"{point.role}: {point.value}")
    if points:
        return get_yaml_string("points_string", points=f"{", ".join(points)}", total_points=total_points)
    return ""


def get_change_points_string(points: Points) -> str:
    """
    Return string, contained change points information

    :param data: points object from Diff
    :type data: Points
    :return: string, contained points information
    :rtype: str
    """
    points_string = []
    for name, from_to in points.root.items():
        from_ = from_to.from_ if from_to.from_ != "?" else 0
        to = from_to.to if from_to.to != "?" else 0
        points_string.append(f'{name}: "{from_}" -> "{to}"')
    return get_yaml_string("change_points_string", points=", ".join(points_string))


# TODO проверить работу изменений комментов
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
    if change.edit_comment_date:
        action = "change"
    return get_yaml_string(
        "comment_change_string", action=get_yaml_string(action), comment_text=get_truncated_string(change.comment_html)
    )


def get_attachment_string(attachments: DiffAttachments) -> str:
    """
    Return string, contained "attachments action" info

    :param attachments: attachmeents object from change
    :type attachments: DiffAttachments
    :return: string message
    :rtype: str
    """
    # if change in one attachement
    # WebHook is not contained filename or another info about attachment
    if attachments.changed:
        return get_yaml_string("attachments_change_string")

    # if new atachment/attachments or delete one attachement
    attr_name = "new"
    action = "create"
    if attachments.deleted:
        attr_name = "deleted"
        action = "delete"
    filenames = ", ".join([file_object.filename for file_object in getattr(attachments, attr_name)])
    return get_yaml_string("attachments_string", action=get_yaml_string(action), filenames=filenames)


def get_from_to_key(diff: Diff, key: str) -> str:
    """
    Check "from", "to" fields and return a key

    :param diff: diff object from change
    :type change: Diff
    :return: string message
    :rtype: str
    """
    if not getattr(diff, key).from_:
        return "from_none"
    if not getattr(diff, key).to:
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

    changes_list = []
    for event in EventChangeEnum:
        match event.value:
            # attachments action in change. Unique change -> make return after parsing
            case "attachments" if change.diff.attachments:
                return get_attachment_string(change.diff.attachments)

            # all other changes may be in combination with other changes in WebHook
            # collect them in a changes_list

            # case "points" if change.diff.points:
            case "points" if getattr(change.diff, "points", None):
                changes_list.append(get_change_points_string(change.diff.points))

            # is_blocked status change
            case "is_blocked" if getattr(change.diff, "is_blocked", None):
                from_to_key = get_from_to_key(change.diff, "is_blocked")
                # block reason text
                reason = get_yaml_string("not_reason")
                # TODO проверить вывод в бота. Если мешают тэги <p></p> - нужно брать поле blocked_note из модели
                if hasattr(change.diff, "blocked_note_html"):
                    reason = get_truncated_string(change.diff.blocked_note_html.to)
                changes_list.append(get_yaml_string(f"change_{event.value}_{from_to_key}_string", reason=reason))

            case _ if getattr(change.diff, event.value, None):
                from_to_key = get_from_to_key(change.diff, event.value)
                from_ = getattr(change.diff, event.value).from_
                to = getattr(change.diff, event.value).to
                # check from_ != to (for estimated_start/finish) fields
                if from_ != to:
                    changes_list.append(
                        get_yaml_string(f"change_{event.value}_{from_to_key}_string", from_=from_, to=to)
                    )

    return "".join(changes_list)


def get_string(payload: WebhookPayload, field: str) -> str:
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
            # check usertstory promoted from "task" or "issue"
            if payload.action == "create" and payload.type == "userstory":
                if payload.data.generated_from_issue:
                    return get_yaml_string("action_userstory_from_issue_string")
                if payload.data.from_task_ref:
                    return get_yaml_string("action_userstory_from_task_string")
            return get_yaml_string("action_string", action=get_yaml_string(payload.action))

        case "object_of_action":
            return get_object_with_url(payload)

        case "parents":
            return get_parents(payload.data)

        case "timestamp":
            return get_yaml_string(
                "action_time_string", timestamp=payload.date.strftime(get_settings().TIMESTAMP_FORMAT)
            )

        case "by_fullname":
            return get_yaml_string("action_author_string", author=payload.by.full_name)

        case "assigned_to" if payload.data.assigned_to:
            return get_assigned_to(payload.data)

        case "change":
            changes = get_changes(payload.change)
            if not changes:
                # TODO вызвать исключение или вернуть текст с ошибкой
                # raise ParsingError(
                #     "Not found template for parsing object payload.change"
                #     f"Change object:\n{payload.change}"
                # )
                return ""
            return get_yaml_string("change_string", changes=changes)

        case "status" if payload.data.status.name:
            return get_yaml_string("status_string", status=payload.data.status.name)

        case "due_date" if payload.data.due_date:
            return get_yaml_string("due_date_string", due_date=payload.data.due_date)

        case "estimated_finish" if payload.data.estimated_finish:
            return get_yaml_string("due_date_string", due_date=payload.data.estimated_finish)

        case "tags" if payload.data.tags:
            return get_yaml_string("tags_string", tags=", ".join(payload.data.tags))

        case "is_iocaine" if payload.data.is_iocaine:
            return get_yaml_string("is_iocaine_string", is_iocaine=payload.data.is_iocaine)

        case "type" if payload.data.type:
            return get_yaml_string("issue_type_string", issue_type=payload.data.type.name)

        case "priority" if payload.data.priority:
            return get_yaml_string("issue_priority_string", priority=payload.data.priority.name)

        case "severity" if payload.data.severity:
            return get_yaml_string("issue_severity_string", severity=payload.data.severity.name)

        case "points":
            return get_points_string(payload.data)

        case "client_requirement" if payload.data.client_requirement:
            return get_yaml_string("client_requirement_string")

        case "team_requirement" if payload.data.team_requirement:
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
    output_fields = get_strings().get("message_schema").get(payload.type).get(payload.action)

    if not output_fields:
        # raise ParsingError(
        #     "Combination of \"type\" and \"action\" fields not found at message_schema"
        #     f"\nInput values:\n- type = {payload.type}\n- action = {payload.action}"
        # )
        # TODO вызвать исключение или вернуть текст с ошибкой
        return ""

    output_message = []
    for text_block in output_fields:
        output_block = []
        for field in text_block:
            field_string = get_string(payload, field)
            # TODO надо разобраться с исключениями. На данный момент если change field_String is None - return ""
            if field == "change" and not field_string:
                return ""
            if field_string:
                output_block.append(field_string)
        if output_block:
            output_message.append("".join(output_block))
    return "\n".join(output_message)


# for development purposes
if __name__ == "__main__":
    with open("tests/entities/fixtures/webhooks/test/issue_to_userstory_change.json", encoding="utf-8") as f:
        input_data = json.load(f)
    event = WebhookPayload.model_validate(input_data)
    print(get_message(event))
