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
from src.utils.text_utils import (
    get_blockquote_tagged_string,
    get_untag_truncated_string,
    get_webhook_notification_text,
)


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
        return ""
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
    if isinstance(data, Epic) or isinstance(data, UserStory) or isinstance(data, Task) or isinstance(data, Issue):
        prefix = f"#{data.ref} "
    else:
        prefix = ""

    if hasattr(data, EventObjectNameField.SUBJECT):
        return prefix + getattr(data, EventObjectNameField.SUBJECT)
    if hasattr(data, EventObjectNameField.NAME):
        return prefix + getattr(data, EventObjectNameField.NAME)
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
    name = get_object_name(data=payload.data)
    named_url = get_named_url(url=payload.data.permalink, name=name, lang=lang)
    blockquote_named_url = get_blockquote_tagged_string(named_url)

    return get_webhook_notification_text(
        text_in_yaml="object_action_url_string",
        lang=lang,
        obj_type=get_webhook_notification_text(text_in_yaml=payload.type, lang=lang),
        named_url=blockquote_named_url,
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
    for parent in EventParentsEnum:
        if hasattr(data, parent) and (parent_object := getattr(data, parent)):
            obj_type = get_webhook_notification_text(text_in_yaml=parent, lang=lang)
            obj_name = get_object_name(data=parent_object)
            named_url = get_named_url(url=parent_object.permalink, name=obj_name, lang=lang)
            parents_list.append(
                get_webhook_notification_text(
                    text_in_yaml="object_with_name_string", lang=lang, obj_type=obj_type, named_url=named_url
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


def get_change_points_string(points: Points, lang: str) -> tuple[str, str]:
    """
    Return a string containing change points information.

    :param points: Points object from Diff object.
    :type points: Points
    :param lang: The language code (key) to select the appropriate translation.
    :type lang: str
    :return: Tuple of strings, containing points information.
    :rtype: tuple[str]
    """

    from_string = []
    to_string = []
    for name, points in points.root.items():
        from_ = points.from_ if points.from_ != "?" else 0
        to = points.to if points.to != "?" else 0
        from_string.append(f'{name}: "{from_}"')
        to_string.append(f'{name}: "{to}"')
    return (
        get_webhook_notification_text(text_in_yaml="change_points_string", lang=lang, points=", ".join(from_string)),
        get_webhook_notification_text(text_in_yaml="change_points_string", lang=lang, points=", ".join(to_string)),
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
    return get_blockquote_tagged_string(
        get_webhook_notification_text(
            text_in_yaml="comment_change_string",
            lang=lang,
            action=get_webhook_notification_text(text_in_yaml=action, lang=lang),
            comment_text=get_untag_truncated_string(change.comment_html),
        )
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
        changes_from_list: list[str] = []
        changes_to_list: list[str] = []

        for current_file in attachments.changed:
            current_file_from_list = [
                get_webhook_notification_text(
                    text_in_yaml="attachments_change_filename",
                    lang=lang,
                    filename=get_named_url(name=current_file.filename, url=current_file.url, lang=lang),
                ),
            ]
            current_file_to_list = [
                get_webhook_notification_text(
                    text_in_yaml="attachments_change_filename",
                    lang=lang,
                    filename=get_named_url(name=current_file.filename, url=current_file.url, lang=lang),
                ),
            ]
            for event in EventAttachmentsChangesField:
                if hasattr(current_file.changes, event) and (changes_object := getattr(current_file.changes, event)):
                    from_, to = changes_object
                    for value, changes in ((from_, current_file_from_list), (to, current_file_to_list)):
                        if isinstance(value, bool):
                            template_name = "label_set" if value else "label_not_set"
                            value = get_webhook_notification_text(text_in_yaml=template_name, lang=lang)
                        elif not value:
                            value = get_webhook_notification_text(text_in_yaml=f"{event.value}_none_string", lang=lang)
                        else:
                            value = get_untag_truncated_string(value)
                        changes.append(
                            get_webhook_notification_text(f"attachments_{event.value}", lang=lang, value=value)
                        )

            for changes, current_changes in (
                (changes_from_list, current_file_from_list),
                (changes_to_list, current_file_to_list),
            ):
                changes.append("".join(current_changes))

        return "⬇️\n".join(
            (
                get_blockquote_tagged_string(
                    get_webhook_notification_text(
                        text_in_yaml="attachments_change_string",
                        lang=lang,
                        action=get_webhook_notification_text(text_in_yaml=action, lang=lang),
                        changes="".join(changes_from_list),
                    )
                ),
                get_blockquote_tagged_string(
                    get_webhook_notification_text(
                        text_in_yaml="attachments_change_string",
                        lang=lang,
                        action=get_webhook_notification_text(text_in_yaml=action, lang=lang),
                        changes="".join(changes_to_list),
                    )
                ),
            )
        )

    # if new attachment/attachments or delete one attachment
    elif attachments.deleted:
        action = EventActionEnum.DELETE
        diff_attachments_list = "deleted"
        files = [current_file.filename for current_file in getattr(attachments, diff_attachments_list)]

    else:
        action = EventActionEnum.CREATE
        diff_attachments_list = "new"
        files = [
            get_named_url(name=current_file.filename, url=current_file.url, lang=lang)
            for current_file in getattr(attachments, diff_attachments_list)
        ]

    return get_blockquote_tagged_string(
        get_webhook_notification_text(
            text_in_yaml="attachments_string",
            lang=lang,
            action=get_webhook_notification_text(text_in_yaml=action, lang=lang),
            filenames=", ".join(files),
        ),
    )


def get_from_to_key(from_to_object: FromTo) -> str:
    """
    Check the "from_" and "to" fields for "null" values and return a key.
    :from_to_object: FromTo object from the change.diff.
    :type from_to_object: FromTo
    :return: String message.
    :rtype: str
    """

    if not from_to_object.from_:
        return "from_none"
    if not from_to_object.to:
        return "to_none"
    return "from_to"


def get_changes(payload: WebhookPayload, lang: str, params: dict[str, dict]) -> str:
    """
    Return strings containing the change information.

    :param payload: Change object from the payload.
    :type payload: WebhookPayload
    :param lang: The language code (key) to select the appropriate translation.
    :type lang: str
    :param params: Additional parameters for message generation.
    :type params: dict[str, dict]
    :return: Message string containing information about changes.
    :rtype: str
    """
    change = payload.change

    # comments action in change. This is a unique change -> return result after parsing.
    if change.comment and "comment" not in params:
        return get_comment_string(change=change, lang=lang)

    # Разобраться с обработкой комментариев и вложений

    changes_from_list = []
    changes_to_list = []

    for event in EventChangeEnum:
        match event:
            # TOD исправить в 2 блока
            # attachments action in change. This is a unique change -> return result after parsing.
            case EventChangeEnum.ATTACHMENTS if attachments := change.diff.attachments:
                return get_attachment_string(attachments=attachments, lang=lang)

            # all other changes may be combined with other changes in the WebHook.
            # collect them in a changes_from/to_list

            # case "points" if change.diff.points:
            case EventChangeEnum.POINTS if points := getattr(change.diff, EventChangeEnum.POINTS, None):
                from_string, to_string = get_change_points_string(points=points, lang=lang)
                changes_from_list.append(from_string)
                changes_to_list.append(to_string)

            # description change
            case EventChangeEnum.DESCRIPTION if getattr(change.diff, EventChangeEnum.DESCRIPTION, None):
                from_ = get_webhook_notification_text(text_in_yaml="data_not_found", lang=lang)

                if not (description_text := payload.data.description):
                    to = get_webhook_notification_text(text_in_yaml="description_diff_none_string", lang=lang)
                else:
                    to = get_untag_truncated_string(description_text)

                for value, changes in ((from_, changes_from_list), (to, changes_to_list)):
                    changes.append(
                        get_webhook_notification_text(
                            text_in_yaml=f"change_{event.value}_string", lang=lang, value=value
                        )
                    )

            # all other changes
            case _ if from_to_object := getattr(change.diff, event, None):
                from_ = from_to_object.from_
                to = from_to_object.to

                # check that the "from_" field is not equal to the "to_" field (for estimated_start/finish).
                if from_ != to:
                    for value, changes in ((from_, changes_from_list), (to, changes_to_list)):
                        if isinstance(value, bool):
                            template_name = "label_set" if value else "label_not_set"
                            value_to_string = get_webhook_notification_text(text_in_yaml=template_name, lang=lang)

                            # check the "reason" field for the "is_blocked" attribute
                            if event == EventChangeEnum.IS_BLOCKED and value:
                                reason = get_webhook_notification_text(text_in_yaml="not_reason_text", lang=lang)
                                if hasattr(change.diff, "blocked_note_html") and getattr(
                                    change.diff, "blocked_note_html"
                                ):
                                    reason = get_untag_truncated_string(change.diff.blocked_note_html.to)
                                value_to_string += get_webhook_notification_text(
                                    text_in_yaml="reason", lang=lang, reason=reason
                                )

                        elif not value:
                            value_to_string = get_webhook_notification_text(
                                text_in_yaml=f"{event.value}_none_string", lang=lang
                            )

                        else:
                            value_to_string = get_untag_truncated_string(
                                ", ".join(value) if isinstance(value, list) else value
                            )

                        changes.append(
                            get_webhook_notification_text(
                                text_in_yaml=f"change_{event.value}_string", lang=lang, value=value_to_string
                            )
                        )

    return "⬇️\n".join(
        (
            get_blockquote_tagged_string(text_string="".join(changes_from_list)),
            get_blockquote_tagged_string(text_string="".join(changes_to_list)),
        )
    )


def get_string(payload: WebhookPayload, field: str, lang: str, params: dict[str, dict] | None) -> str:
    """
    Return a parsed string from the WebhookPayload object data.

    :param payload: Payload from the webhook.
    :type payload: WebhookPayload
    :param field: Field to be parsed.
    :type field: str
    :param lang: The language code (key) to select the appropriate translation.
    :type lang: str
    :param params: Additional parameters for message generation.
    :type params: dict[str, dict]
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
            timestamp = payload.date.strftime(get_settings().TIMESTAMP_FORMAT)
            if aggregated_date := params.get("aggregated_date"):
                first_event_datetime = aggregated_date["first_event_datetime"].strftime(get_settings().TIME_FORMAT)
                last_event_datetime = aggregated_date["last_event_datetime"].strftime(get_settings().TIMESTAMP_FORMAT)
                timestamp = f"{first_event_datetime} - {last_event_datetime}"
            return get_webhook_notification_text(
                text_in_yaml="action_time_string",
                lang=lang,
                timestamp=timestamp,
            )

        case EventFieldsEnum.BY_FULLNAME:
            author = payload.by.full_name
            if aggregated_by_fullname := params.get("aggregated_by"):
                author = aggregated_by_fullname
            return get_webhook_notification_text(text_in_yaml="action_author_string", lang=lang, author=author)

        case EventFieldsEnum.ASSIGNED_TO if payload.data.assigned_to:
            return get_assigned_to_string(data=payload.data, lang=lang)

        case EventFieldsEnum.CHANGE:
            changes = get_changes(payload=payload, lang=lang, params=params)
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

        case EventFieldsEnum.DESCRIPTION if payload.data.description:
            return get_webhook_notification_text(
                text_in_yaml="description_string",
                lang=lang,
                description=get_blockquote_tagged_string(get_untag_truncated_string(payload.data.description)),
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
            reason = get_webhook_notification_text(text_in_yaml="not_reason_text", lang=lang)
            if payload.data.blocked_note:
                reason = get_untag_truncated_string(payload.data.blocked_note)
            return get_webhook_notification_text(text_in_yaml="is_blocked_string", lang=lang, reason=reason)

        case EventFieldsEnum.TEST:
            return get_webhook_notification_text(text_in_yaml="test_string", lang=lang, test=payload.data.test)

    return ""


def get_message(payload: WebhookPayload, lang: str, params: dict[str, dict]) -> tuple[str, list[DiffBaseAttachment]]:
    """
    Return a message containing information from the WebhookPayload object data.

    :param payload: Payload from the webhook.
    :type payload: WebhookPayload
    :param lang: The language code (key) to select the appropriate translation.
    :type lang: str
    :param params: Additional parameters for message generation.
    :type params: dict[str, dict]
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
            field_string = get_string(payload=payload, field=field, lang=lang, params=params)
            if field_string:
                output_block.append(field_string)
        if output_block:
            output_message.append("".join(output_block))

    return "\n".join(output_message), new_attachments
