from datetime import datetime

from src.core.Base.exceptions import MessageFormatterError
from src.core.settings import get_settings, get_strings
from src.entities.enums.event_enums import (
    EventActionEnum,
    EventAttachmentsChangesField,
    EventChangeEnum,
    EventFieldsEnum,
    EventObjectNameField,
    EventParentsEnum,
    EventTypeEnum,
)
from src.entities.schemas.webhook_data.diff_webhook_schemas import (
    DiffAttachments,
    DiffBaseAttachment,
    Points,
)
from src.entities.schemas.webhook_data.nested_schemas import (
    Epic,
    FromTo,
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
from src.utils.text_utils import clean_string, get_webhook_notification_text


def get_untag_truncated_string(text: str) -> str:
    """
    Remove tags and truncate the string if its length exceeds the specified value.

    :param text: String to process.
    :type text: str
    :returns: String with removed tags, not exceeding the specified length.
    :rtype: str
    """

    tags = ("<p>", "</p>")
    for tag in tags:
        text = text.replace(tag, "")

    maximum_text_length = get_settings().TRUNCATED_STRING_LENGTH
    if len(text) > maximum_text_length:
        return text[:maximum_text_length] + "..."
    return text


def get_named_url(url: str, name: str, lang: str) -> str:
    """
    Returns a string containing the object's name and permalink.

    :param url: String containing the object's permalink.
    :type url: str
    :param name: String containing the object's name.
    :type name: str
    :param lang: The language code (key) to select the appropriate translation.
    :type lang: str
    :returns: String containing the object's name and permalink.
    :rtype: str
    """

    if not name:
        name = get_webhook_notification_text(text_in_yaml="link", lang=lang)
    return f'<a href="{url}">{name}</a>'


def get_object_name(data: Milestone | Epic | UserStory | Task | Issue | Wiki) -> str:
    """
    Return the object name.

    Get the object name from the "name" (for Milestone) or "subject" (for all other objects) field, or None (for Wiki).

    :param data: Data object from payload.
    :type data: Milestone, Epic, UserStory, Task, Issue, Wiki
    :returns: String containing the object's name or empty string.
    :rtype: str
    """
    if hasattr(data, EventObjectNameField.SUBJECT):
        return getattr(data, EventObjectNameField.SUBJECT)
    if hasattr(data, EventObjectNameField.NAME):
        return getattr(data, EventObjectNameField.NAME)
    return ""


def get_object_with_url(payload: WebhookPayload, lang: str) -> str:
    """
    Return a string from the template, containing the type, name (if defined), and URL of the object.

    :param payload: Payload object from the Webhook.
    :type payload: WebhookPayload
    :param lang: The language code (key) to select the appropriate translation.
    :type lang: str
    :return: String from the template.
    :rtype: str
    """

    return get_webhook_notification_text(
        text_in_yaml="object_action_url_string",
        lang=lang,
        obj_type=get_webhook_notification_text(text_in_yaml=payload.type, lang=lang),
        named_url=get_named_url(url=payload.data.permalink, name=get_object_name(data=payload.data), lang=lang),
    )


def get_parents_string(data: Milestone | Epic | UserStory | Task | Issue | Wiki, lang: str) -> str:
    """
    Return a string containing the parents of objects.

    :param data: Data object from the payload.
    :type data: Milestone, Epic, UserStory, Task, Issue, Wiki
    :param lang: The language code (key) to select the appropriate translation.
    :type lang: str
    :return: String containing the parents of objects.
    :rtype: str
    """

    parents_list = []
    for parent_type in EventParentsEnum:
        if hasattr(data, parent_type) and (parent_object := getattr(data, parent_type)):
            parents_list.append(
                get_webhook_notification_text(
                    text_in_yaml="object_with_name_string",
                    lang=lang,
                    obj_type=get_webhook_notification_text(text_in_yaml=parent_type, lang=lang),
                    obj_name=get_object_name(data=parent_object),
                )
            )
    return "".join(parents_list)


def get_assigned_to_string(data: Milestone | Epic | UserStory | Task | Project | Issue | Wiki, lang: str) -> str:
    """
    Return a string containing the "assigned_to" information.

    :param data: Data object from the payload.
    :type data: Milestone, Epic, UserStory, Task, Issue, Wiki
    :param lang: The language code (key) to select the appropriate translation.
    :type lang: str
    :return: String containing the "assigned_to" information.
    :rtype: str
    """

    assigned_suffix = ""
    # if the object "assigned to" more than one user, add information about the number of users
    if hasattr(data, "assigned_users") and (count_assigned_users := len(data.assigned_users)) > 1:
        assigned_suffix = f" + {count_assigned_users - 1}"
    return get_webhook_notification_text(
        text_in_yaml="assigned_to_string", lang=lang, assigned=(data.assigned_to.full_name + assigned_suffix)
    )


def get_points_string(data: Milestone | Epic | UserStory | Task | Project | Wiki | Issue, lang: str) -> str:
    """
    Return a string containing points information and the calculated total points.

    :param data: Data object from the payload.
    :type data: Milestone, Epic, UserStory, Task, Issue, Wiki
    :param lang: The language code (key) to select the appropriate translation.
    :type lang: str
    :return: String containing points information.
    :rtype: str
    """

    total_points = 0
    points = []
    for point in data.points:
        if point.value:
            total_points += point.value
            points.append(f"{point.role}: {point.value}")
    if points:
        return get_webhook_notification_text(
            text_in_yaml="points_string", lang=lang, points=f"{", ".join(points)}", total_points=total_points
        )
    return ""


def get_change_points_string(points: Points, lang: str) -> str:
    """
    Return a string containing change points information.

    :param points: Points object from Diff object.
    :type points: Points
    :param lang: The language code (key) to select the appropriate translation.
    :type lang: str
    :return: String containing points information.
    :rtype: str
    """

    points_string = []
    for name, from_to in points.root.items():
        from_ = from_to.from_ if from_to.from_ != "?" else 0
        to = from_to.to if from_to.to != "?" else 0
        points_string.append(f'{name}: "{from_}" -> "{to}"')
    return get_webhook_notification_text(
        text_in_yaml="change_points_string", lang=lang, points=", ".join(points_string)
    )


def get_comment_string(change: Change, lang: str) -> str:
    """
    Return a string containing "comments action" information.

    :param change: Change object from the payload.
    :type change: Change
    :param lang: The language code (key) to select the appropriate translation.
    :type lang: str
    :return: String message.
    :rtype: str
    """

    if change.delete_comment_date:
        action = EventActionEnum.DELETE
    elif change.edit_comment_date:
        action = EventActionEnum.CHANGE
    else:
        action = EventActionEnum.CREATE
    return get_webhook_notification_text(
        text_in_yaml="comment_change_string",
        lang=lang,
        action=get_webhook_notification_text(text_in_yaml=action, lang=lang),
        comment_text=get_untag_truncated_string(change.comment_html),
    )


def get_attachment_string(attachments: DiffAttachments, lang: str) -> str:
    """
    Return a string containing "attachments action" information.

    :param attachments: Attachments object from the change.
    :type attachments: DiffAttachments
    :param lang: The language code (key) to select the appropriate translation.
    :type lang: str
    :return: String message.
    :rtype: str
    """

    # if there is a change in one attachment
    if attachments.changed:
        action = EventActionEnum.CHANGE
        changes_list = []
        for current_file in attachments.changed:
            current_file_changes = []
            for event in EventAttachmentsChangesField:
                if hasattr(current_file.changes, event) and (changes_object := getattr(current_file.changes, event)):
                    from_, to = changes_object
                    from_to_key = get_from_to_key(FromTo(from_=from_, to=to))
                    current_file_changes.append(
                        get_webhook_notification_text(
                            f"attachments_{event.value}_{from_to_key}", lang=lang, from_=from_, to=to
                        )
                    )
            changes_list.append(
                get_webhook_notification_text(
                    text_in_yaml="attachments_change_string",
                    lang=lang,
                    action=get_webhook_notification_text(text_in_yaml=action, lang=lang),
                    filename=current_file.filename,
                    attachment_changes=", ".join(current_file_changes),
                )
            )
        return "".join(changes_list)

    # if new attachment/attachments or delete one attachment
    if attachments.deleted:
        action = EventActionEnum.DELETE
        diff_attachments_list = "deleted"
    else:
        action = EventActionEnum.CREATE
        diff_attachments_list = "new"

    return get_webhook_notification_text(
        text_in_yaml="attachments_string",
        lang=lang,
        action=get_webhook_notification_text(text_in_yaml=action, lang=lang),
        filenames=", ".join([current_file.filename for current_file in getattr(attachments, diff_attachments_list)]),
    )


def get_from_to_key(from_to_object: FromTo) -> str:
    """
    Check the "from_" and "to" fields for "null" values and return a key.
    :from_to_object: FromTo object from the change.diff.
    :type diff: FromTo
    :return: String message.
    :rtype: str
    """

    if not from_to_object.from_:
        return "from_none"
    if not from_to_object.to:
        return "to_none"
    return "from_to"


def get_changes(change: Change, lang: str) -> str:
    """
    Return strings containing the change information.

    :param change: Change object from the payload.
    :type change: Change
    :param lang: The language code (key) to select the appropriate translation.
    :type lang: str
    :return: Message string containing information about changes.
    :rtype: str
    """

    # comments action in change. This is a unique change -> return result after parsing.
    if change.comment:
        return get_comment_string(change=change, lang=lang)

    changes_list = []
    for event in EventChangeEnum:
        match event:
            # attachments action in change. This is a unique change -> return result after parsing.
            case EventChangeEnum.ATTACHMENTS if attachments := change.diff.attachments:
                return get_attachment_string(attachments=attachments, lang=lang)

            # all other changes may be combined with other changes in the WebHook.
            # collect them in a changes_list

            # case "points" if change.diff.points:
            case EventChangeEnum.POINTS if points := getattr(change.diff, EventChangeEnum.POINTS, None):
                changes_list.append(get_change_points_string(points=points, lang=lang))

            # is_blocked status change
            case EventChangeEnum.IS_BLOCKED if diff_attribute := getattr(change.diff, EventChangeEnum.IS_BLOCKED, None):
                from_to_key = get_from_to_key(from_to_object=diff_attribute)
                # block reason text
                reason = get_webhook_notification_text(text_in_yaml="not_reason", lang=lang)
                if hasattr(change.diff, "blocked_note_html"):
                    reason = get_untag_truncated_string(change.diff.blocked_note_html.to)
                changes_list.append(
                    get_webhook_notification_text(
                        text_in_yaml=f"change_{event.value}_{from_to_key}_string", lang=lang, reason=reason
                    )
                )

            case _ if from_to_object := getattr(change.diff, event, None):
                from_to_key = get_from_to_key(from_to_object)
                from_ = clean_string(from_to_object.from_)
                to = clean_string(from_to_object.to)
                # check that the "from_" field is not equal to the "to_" field (for estimated_start/finish).
                if from_ != to:
                    changes_list.append(
                        get_webhook_notification_text(
                            text_in_yaml=f"change_{event.value}_{from_to_key}_string", lang=lang, from_=from_, to=to
                        )
                    )

    return "".join(changes_list)


def get_string(payload: WebhookPayload, field: str, lang: str) -> str:
    """
    Return a parsed string from the WebhookPayload object data.

    :param payload: Payload from the webhook.
    :type payload: WebhookPayload
    :param field: Field to be parsed.
    :type field: str
    :param lang: The language code (key) to select the appropriate translation.
    :type lang: str
    :return: Parsed string.
    :rtype: str
    :raises MessageFormatterError: If the get_changes function returns an empty string.
    """

    match field:
        case EventFieldsEnum.ACTION:
            # check userstory promoted from "task" or "issue"
            if payload.action == EventActionEnum.CREATE and payload.type == EventTypeEnum.USERSTORY:
                if payload.data.generated_from_issue:
                    return get_webhook_notification_text(text_in_yaml="action_userstory_from_issue_string", lang=lang)
                if payload.data.from_task_ref:
                    return get_webhook_notification_text(text_in_yaml="action_userstory_from_task_string", lang=lang)
            return get_webhook_notification_text(
                text_in_yaml="action_string",
                lang=lang,
                action=get_webhook_notification_text(text_in_yaml=payload.action, lang=lang),
            )

        case EventFieldsEnum.OBJECT_OF_ACTION:
            return get_object_with_url(payload=payload, lang=lang)

        case EventFieldsEnum.PARENTS:
            return get_parents_string(data=payload.data, lang=lang)

        case EventFieldsEnum.TIMESTAMP:
            return get_webhook_notification_text(
                text_in_yaml="action_time_string",
                lang=lang,
                timestamp=payload.date.strftime(get_settings().TIMESTAMP_FORMAT),
            )

        case EventFieldsEnum.BY_FULLNAME:
            return get_webhook_notification_text(
                text_in_yaml="action_author_string", lang=lang, author=payload.by.full_name
            )

        case EventFieldsEnum.ASSIGNED_TO if payload.data.assigned_to:
            return get_assigned_to_string(data=payload.data, lang=lang)

        case EventFieldsEnum.CHANGE:
            changes = get_changes(change=payload.change, lang=lang)
            if not changes:
                raise MessageFormatterError(
                    "\nThe function get_changes returned an empty message. "
                    'The "payload.change" object is missing fields for which processing templates are described.'
                    f"\nInput values:\n- payload.change object: \n{payload.change}"
                )
            return get_webhook_notification_text(text_in_yaml="change_string", lang=lang, changes=changes)

        case EventFieldsEnum.STATUS:
            return get_webhook_notification_text(
                text_in_yaml="status_string", lang=lang, status=payload.data.status.name
            )

        case EventFieldsEnum.DUE_DATE if payload.data.due_date:
            return get_webhook_notification_text(
                text_in_yaml="due_date_string", lang=lang, due_date=str(datetime.date(payload.data.due_date))
            )

        case EventFieldsEnum.ESTIMATED_FINISH:
            return get_webhook_notification_text(
                text_in_yaml="due_date_string", lang=lang, due_date=str(payload.data.estimated_finish)
            )

        case EventFieldsEnum.TAGS if payload.data.tags:
            return get_webhook_notification_text(
                text_in_yaml="tags_string", lang=lang, tags=", ".join(payload.data.tags)
            )

        case EventFieldsEnum.IS_IOCAINE if payload.data.is_iocaine:
            return get_webhook_notification_text(text_in_yaml="is_iocaine_string", lang=lang)

        case EventFieldsEnum.TYPE:
            return get_webhook_notification_text(
                text_in_yaml="issue_type_string", lang=lang, issue_type=payload.data.type.name
            )

        case EventFieldsEnum.PRIORITY:
            return get_webhook_notification_text(
                text_in_yaml="issue_priority_string", lang=lang, priority=payload.data.priority.name
            )

        case EventFieldsEnum.SEVERITY:
            return get_webhook_notification_text(
                text_in_yaml="issue_severity_string", lang=lang, severity=payload.data.severity.name
            )

        case EventFieldsEnum.POINTS:
            return get_points_string(data=payload.data, lang=lang)

        case EventFieldsEnum.CLIENT_REQUIREMENT if payload.data.client_requirement:
            return get_webhook_notification_text(text_in_yaml="client_requirement_string", lang=lang)

        case EventFieldsEnum.TEAM_REQUIREMENT if payload.data.team_requirement:
            return get_webhook_notification_text(text_in_yaml="team_requirement_string", lang=lang)

        case EventFieldsEnum.IS_BLOCKED if payload.data.is_blocked:
            return get_webhook_notification_text(text_in_yaml="is_blocked_string", lang=lang)

    return ""


def get_message(payload: WebhookPayload, lang: str) -> tuple[str, list[DiffBaseAttachment]]:
    """
    Return a message containing information from the WebhookPayload object data.

    :param payload: Payload from the webhook.
    :type payload: WebhookPayload
    :param lang: The language code (key) to select the appropriate translation.
    :type lang: str
    :return: Tuple containing a text string message and a list of DiffBaseAttachment objects,
    which will be empty if no new attachments were added.
    :rtype: tuple[str, list[DiffBaseAttachment]]
    :raises MessageFormatterError: If template for parsing data from the payload object was not found.
    """
    output_fields = get_strings().get("message_schema").get(payload.type).get(payload.action)

    if not output_fields:
        raise MessageFormatterError(
            "The template for parsing data from the payload object was not found."
            f"\nInput values:\n- type = {payload.type}\n- action = {payload.action}"
        )

    new_attachments: list[DiffBaseAttachment] = []
    # if the action is "change" and "new" is present in change.diff.attachments create list[DiffBaseAttachment] object
    if (
        payload.action == EventActionEnum.CHANGE
        and hasattr(payload.change.diff, "attachments")
        and hasattr(payload.change.diff.attachments, "new")
        and (attachments_list := payload.change.diff.attachments.new)
    ):
        new_attachments = [
            DiffBaseAttachment(filename=new_file.filename, url=new_file.url) for new_file in attachments_list
        ]

    output_message = []
    for text_block in output_fields:
        output_block = []
        for field in text_block:
            field_string = get_string(payload=payload, field=field, lang=lang)
            if field_string:
                output_block.append(field_string)
        if output_block:
            output_message.append("".join(output_block))

    return "\n".join(output_message), new_attachments
