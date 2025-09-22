import json

from src.entities.enums.event_enums import EventActionEnum, EventChangeEnum
from src.entities.schemas.webhook_data.webhook_payload_schemas import WebhookPayload


def _aggregate_comment_fields(
    current_change: dict, action_date: int, aggregated_comments: dict[str, dict]
) -> dict[str, dict]:
    """
    Under development
    """
    current_comment_html = current_change["comment_html"]

    added = aggregated_comments["added"]
    changed = aggregated_comments["changed"]
    deleted = aggregated_comments["deleted"]

    if current_change["delete_comment_date"]:
        if current_comment_html in added:
            added.pop(current_comment_html)
        else:
            deleted["current_comment_html"] = action_date

    elif current_change["edit_comment_date"]:
        is_current_comment_at_added_or_edited_comments = False
        for previous_comment in current_change["comment_versions"]:
            previous_comment_html = previous_comment["comment_html"]
            if previous_comment_html in added:
                is_current_comment_at_added_or_edited_comments = True
                added[current_comment_html] = action_date
                added.pop(previous_comment_html)
                break
            elif previous_comment_html in changed:
                is_current_comment_at_added_or_edited_comments = True
                changed[current_comment_html] = action_date
                changed.pop(previous_comment_html)
                break
        if not is_current_comment_at_added_or_edited_comments:
            changed[current_comment_html] = action_date
    elif current_comment_html:
        added[current_comment_html] = action_date

    return {"added": added, "changed": changed, "deleted": deleted}


def _aggregate_attachments_fields(aggregated_attachments: dict, current_attachments: dict) -> None:
    """Under development."""
    # в текущем вебхуке добавлены новые вложения - добавляем их в список новых вложений агрегированного вебхука
    if current_attachments["new"]:
        aggregated_attachments["new"].extend(current_attachments["new"])
    # TOD проверить в удаленных и разобраться с восстановлением комментов, когда он придет новым вебхуком "создание"

    # в текущем вебхуке изменения во вложениях
    elif current_attachments["changed"]:
        for file_in_changed_wh in current_attachments["changed"]:
            is_in_new_aggregated_attachments = False
            # если измененные вложения содержатся в "новых" в сборном вебхуке, то обновляем поля в списке "новых"
            for file_in_new_aggregated_wh in aggregated_attachments["new"]:
                if file_in_changed_wh["url"] == file_in_new_aggregated_wh["url"]:
                    for key in ["description", "is_deprecated"]:
                        if key in file_in_changed_wh["changes"]:
                            file_in_new_aggregated_wh["description"] = file_in_changed_wh["changes"]["description"][-1]
                            file_in_new_aggregated_wh["is_deprecated"] = file_in_changed_wh["changes"]["is_deprecated"][
                                -1
                            ]
                    is_in_new_aggregated_attachments = True
                    break

            if is_in_new_aggregated_attachments:
                break

            # если измененные вложения содержатся в "измененных" в сборном вебхуке,
            # то вызываем вспомогательную функцию агрегатор
            for file_in_changed_aggregated_wh in aggregated_attachments["changed"]:
                if file_in_changed_wh["url"] == file_in_changed_aggregated_wh["url"]:
                    for key in ["description", "is_deprecated"]:
                        _aggregate_from_to_field(
                            aggregated_instance=file_in_changed_aggregated_wh["changes"],
                            current_key=key,
                            current_value=file_in_changed_wh[key],
                        )

    elif current_attachments["deleted"]:
        for file_in_deleted_wh in current_attachments["delete"]:
            is_in_new_aggregated_attachments = False
            for file_in_new_aggregated_list in aggregated_attachments["new"]:
                if file_in_deleted_wh["url"] == file_in_new_aggregated_list["url"]:
                    aggregated_attachments["new"].remove(file_in_new_aggregated_list)
                    is_in_new_aggregated_attachments = True
                    break

            if is_in_new_aggregated_attachments:
                break

            for file_in_changed_aggregated_list in aggregated_attachments["changed"]:
                if file_in_deleted_wh["url"] == file_in_changed_aggregated_list["url"]:
                    aggregated_attachments["changed"].remove(file_in_changed_aggregated_list)

            aggregated_attachments["deleted"].append(file_in_deleted_wh)


def _aggregate_from_to_field(aggregated_instance: dict, current_key: str, current_value: dict) -> None:
    """
    Aggregates a 'from-to' change field within a dictionary by updating or removing entries based on value transitions.

    :param aggregated_instance: The dictionary holding aggregated 'from-to' change fields.
    :type aggregated_instance: dict
    :param current_key: The key corresponding to the field to aggregate.
    :type current_key: str
    :param current_value: A dictionary with "from" and "to" keys representing the current change.
    :type current_value: dict
    """
    if not aggregated_instance.get(current_key):
        aggregated_instance[current_key] = current_value
    elif aggregated_instance[current_key]["from"] == current_value["to"]:
        aggregated_instance.pop(current_key)
    else:
        aggregated_instance[current_key]["to"] = current_value["to"]


def _is_contained_changes(diff: dict, params: dict) -> bool:
    """
    Checks whether there are any changes present in the given diff or in the params dictionary.

    :param diff: A dictionary representing the differences/changes.
    :type diff: dict
    :param params: A dictionary of additional parameters which may include aggregated comments.
    :type params: dict
    :return: True if changes are detected in diff or in the params; otherwise False.
    :rtype: bool
    """
    is_changes_in_diff = False
    for _, value in diff.items():
        if value:
            is_changes_in_diff = True
    return is_changes_in_diff or "aggregated_comments" in params


def aggregate_wh_list(wh_data_sorted_list: list[str]) -> tuple[WebhookPayload, dict]:
    """
    Aggregates a list of webhook events into a single aggregated webhook with additional parameters.

    :param wh_data_sorted_list: A time-sorted list of JSON strings, each representing a webhook event.
    :type wh_data_sorted_list: list[str]
    :return: A tuple containing the aggregated WebhookPayload instance and a dictionary of additional parameters.
    :rtype: tuple[WebhookPayload, dict]
    """

    params: dict = {}

    if len(wh_data_sorted_list) == 1:
        return WebhookPayload(**json.loads(wh_data_sorted_list[0])), params

    if json.loads(wh_data_sorted_list[-1])["action"] == EventActionEnum.DELETE:
        return WebhookPayload(**json.loads(wh_data_sorted_list[-1])), params

    aggregated_wh = json.loads(wh_data_sorted_list[0])
    first_event_datetime = aggregated_wh["date"]
    last_event_datetime = aggregated_wh["date"]
    action_by_fullnames = [
        aggregated_wh["by"]["full_name"],
    ]
    action_by_ids = {
        aggregated_wh["by"]["id"],
    }
    first_event_description = aggregated_wh["data"].get("description")
    last_event_description = first_event_description
    aggregated_comments = {"added": {}, "changed": {}, "deleted": {}}

    for current_wh_data in wh_data_sorted_list[1:]:
        current_wh_json_data = json.loads(current_wh_data)

        if current_wh_json_data["action"] == EventActionEnum.DELETE:
            return WebhookPayload(**current_wh_json_data), params

        if current_wh_json_data["by"]["id"] not in action_by_ids:
            action_by_fullnames.append(current_wh_json_data["by"]["full_name"])
            action_by_ids.add(current_wh_json_data["by"]["id"])
        last_event_datetime = current_wh_json_data["date"]

        aggregated_wh["data"] = current_wh_json_data["data"]

        current_diffs = current_wh_json_data["change"]["diff"]
        for key, value in current_diffs.items():
            if key == EventChangeEnum.DESCRIPTION and value:
                aggregated_wh["change"]["diff"][key] = value
                last_event_description = aggregated_wh["data"]["description"]
            elif key == EventChangeEnum.POINTS and value:
                if not aggregated_wh["change"]["diff"]["points"]:
                    aggregated_wh["change"]["diff"]["points"] = {}
                for points_key, points_value in value.items():
                    _aggregate_from_to_field(
                        aggregated_instance=aggregated_wh["change"]["diff"]["points"],
                        current_key=points_key,
                        current_value=points_value,
                    )
            elif value and value["from"] != value["to"]:
                _aggregate_from_to_field(
                    aggregated_instance=aggregated_wh["change"]["diff"], current_key=key, current_value=value
                )

        if current_attachments := current_diffs.get(EventChangeEnum.ATTACHMENTS):
            _aggregate_attachments_fields(
                aggregated_attachments=aggregated_wh["change"]["diff"]["attachments"],
                current_attachments=current_attachments,
            )

        aggregated_comments = _aggregate_comment_fields(
            current_change=current_wh_json_data["change"],
            action_date=current_wh_json_data["date"],
            aggregated_comments=aggregated_comments,
        )

    if first_event_description == last_event_description and "description" in aggregated_wh["change"]["diff"]:
        aggregated_wh["change"]["diff"].pop("description")

    if aggregated_comments["added"] or aggregated_comments["changed"] or aggregated_comments["deleted"]:
        params["aggregated_comments"] = aggregated_comments

    if not _is_contained_changes(diff=aggregated_wh["change"]["diff"], params=params):
        params["no_aggregate_changes"] = True

    if len(action_by_fullnames) != 1:
        params["aggregated_by"] = ", ".join(action_by_fullnames)

    if first_event_description != last_event_description:
        params["aggregated_date"] = {
            "first_event_datetime": first_event_datetime,
            "last_event_datetime": last_event_datetime,
        }

    return WebhookPayload(**aggregated_wh), params
