import json
from datetime import datetime
from logging import Formatter

from c42eventextractor.maps import (
    FILE_EVENT_TO_SIGNATURE_ID_MAP,
    CEF_CUSTOM_FIELD_NAME_MAP,
    JSON_TO_CEF_MAP,
)

CEF_TEMPLATE = u"CEF:0|Code42|{productName}|1|{signatureID}|{eventName}|{severity}|{extension}"
CEF_TIMESTAMP_FIELDS = ["end", "fileCreateTime", "fileModificationTime", "rt"]


class FileEventDictToCEFFormatter(Formatter):
    """Formats file event dicts into CEF format. Attach to a logger via `setFormatter` to use.

    Args:
        default_product_name: The default value to use in the product name segment of the CEF message.
        default_severity_level: The default integer between 1 and 10 to assign to the severity segment of the CEF message.
    """

    def __init__(
        self, default_product_name="Advanced Exfiltration Detection", default_severity_level="5"
    ):
        # type: (str, str) -> None
        super(FileEventDictToCEFFormatter, self).__init__()
        self._default_product_name = default_product_name
        self._default_severity_level = default_severity_level

    def format(self, record):
        file_event_dict = record.msg
        # security events must convert to file event dict format before calling this.
        kvp_list = {
            JSON_TO_CEF_MAP[key]: file_event_dict[key]
            for key in file_event_dict
            if key in JSON_TO_CEF_MAP
            and (file_event_dict[key] is not None and file_event_dict[key] != [])
        }

        extension = u" ".join(_format_cef_kvp(key, kvp_list[key]) for key in kvp_list)

        event_name = file_event_dict.get("eventType", "UNKNOWN")
        signature_id = FILE_EVENT_TO_SIGNATURE_ID_MAP.get(event_name, "C42000")

        cef_log = CEF_TEMPLATE.format(
            productName=self._default_product_name,
            signatureID=signature_id,
            eventName=event_name,
            severity=self._default_severity_level,
            extension=extension,
        )
        return cef_log


class FileEventDictToJSONFormatter(Formatter):
    """Formats file event dicts into JSON format. Attach to a logger via `setFormatter` to use.

    Items in the dictionary whose values are `None`, empty string, or empty lists will be excluded
    from the JSON conversion.
    """

    def format(self, record):
        file_event_dict = record.msg
        file_event_dict = {
            key: file_event_dict[key]
            for key in file_event_dict
            if file_event_dict[key] or file_event_dict[key] == 0
        }
        return json.dumps(file_event_dict)


class FileEventDictToRawJSONFormatter(Formatter):
    """Formats file event dicts into JSON format. Attach to a logger via `setFormatter` to use."""

    def format(self, record):
        return json.dumps(record.msg)


def _format_cef_kvp(cef_field_key, cef_field_value):
    if cef_field_key + "Label" in CEF_CUSTOM_FIELD_NAME_MAP:
        return _format_custom_cef_kvp(cef_field_key, cef_field_value)

    cef_field_value = _handle_nested_json_fields(cef_field_key, cef_field_value)
    if isinstance(cef_field_value, list):
        cef_field_value = _convert_list_to_csv(cef_field_value)
    elif cef_field_key in CEF_TIMESTAMP_FIELDS:
        cef_field_value = _convert_file_event_timestamp_to_cef_timestamp(cef_field_value)
    return u"{0}={1}".format(cef_field_key, cef_field_value)


def _handle_nested_json_fields(cef_field_key, cef_field_value):
    result = []
    if cef_field_key == u"duser":
        result = [item[u"cloudUsername"] for item in cef_field_value if type(item) is dict]

    return result or cef_field_value


def _format_custom_cef_kvp(custom_cef_field_key, custom_cef_field_value):
    custom_cef_label_key = "{0}Label".format(custom_cef_field_key)
    custom_cef_label_value = CEF_CUSTOM_FIELD_NAME_MAP[custom_cef_label_key]
    return u"{0}={1} {2}={3}".format(
        custom_cef_field_key, custom_cef_field_value, custom_cef_label_key, custom_cef_label_value
    )


def _convert_list_to_csv(_list):
    value = u",".join([val for val in _list])
    return value


def _convert_file_event_timestamp_to_cef_timestamp(timestamp_value):
    try:
        _datetime = datetime.strptime(timestamp_value, "%Y-%m-%dT%H:%M:%S.%fZ")
    except ValueError:
        _datetime = datetime.strptime(timestamp_value, "%Y-%m-%dT%H:%M:%SZ")
    value = "{:.0f}".format(_datetime_to_ms_since_epoch(_datetime))
    return value


def _datetime_to_ms_since_epoch(_datetime):
    epoch = datetime.utcfromtimestamp(0)
    total_seconds = (_datetime - epoch).total_seconds()
    # total_seconds will be in decimals (millisecond precision)
    return total_seconds * 1000
