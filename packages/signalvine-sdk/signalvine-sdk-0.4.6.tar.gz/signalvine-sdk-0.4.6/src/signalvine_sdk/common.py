import csv
import hmac
import hashlib
import base64
import logging
import pandas as pd
from typing import Dict, List
from datetime import datetime, timezone
from box import Box

LOGGER = logging.getLogger(__name__)


class Error(Exception):
    """Base class for other exceptions"""

    pass


class APIError(Error):
    """Exception raised in the API call.

    Attributes:
        status_code -- HTTP status code
        message -- text message of the error
    """

    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message


def build_headers(
    token: str,
    secret: str,
    action: str = "GET",
    path_no_query: str = "",
    body: str = "",
) -> Dict:

    now_date = datetime.now(timezone.utc).isoformat()

    auth_string = sign_request(token, secret, now_date, action, path_no_query, body)
    auth_header = f"SignalVine {token}:{auth_string}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": auth_header,
        "SignalVine-Date": now_date,
    }

    return headers


def sign_request(
    token: str,
    secret: str,
    timestamp: str,
    action: str,
    path_no_query: str,
    body: str = "",
) -> str:
    """
    Sign the request and return a bearer token for the SignalVine API

    Return a string with the encrypted request string
    """
    string_to_sign = f"{token}\n{action}\n{path_no_query}\n{body}\n{timestamp}".lower()

    digest = hmac.new(
        secret.encode(), msg=string_to_sign.encode(), digestmod=hashlib.sha256
    ).digest()
    signature = base64.b64encode(digest).decode()

    return signature


def convert_participant_to_record(item, include_agg: bool = False) -> Dict:
    """
    Take the items from JSON and convert into a final data structure for analysis.
    """
    record = {}
    boxed_item = Box(item)

    for profile in boxed_item.profile:
        # These are a mix of custom and vendor-provided profile fields.
        if profile.value:
            record[f"{profile.name}"] = profile.value
        else:
            record[f"{profile.name}"] = None

    if include_agg:
        # Including these because these are handy to have, without
        # grabbing the entire message content and aggregating.
        record["agg_receivedCount"] = boxed_item.receivedCount
        record["agg_scheduledCount"] = boxed_item.scheduledCount
        record["agg_sentCount"] = boxed_item.sentCount

    return record


def convert_participants_to_records(items, include_agg: bool = False) -> List:
    """
    Take all the items from JSON and convert into a final data structure.
    """
    new_list = []
    for item in items:
        record = convert_participant_to_record(item, include_agg)
        new_list.append(record)

    return new_list


def make_body(
    program_id: str,
    content_df: pd.DataFrame,
    new_flag: str = "add",
    mode_flag: str = "tx",
):
    """
    From https://support.signalvine.com/hc/en-us/articles/360023207353-API-documentation

    new_flag can be 'add' or 'ignore'
    mode_flag can be 'tx' or 'row'

    """
    contents = content_df.to_csv(index=False, line_terminator="\n")
    columns = content_df.columns.tolist()

    if not columns:
        columns = "ignore"

    body = {
        "program": f"{program_id}",
        "options": {
            "new": new_flag,
            "mode": mode_flag,
            "existing": columns,
            "absent": "ignore",
        },
        "participants": f"{contents}",
    }

    return body


def convert_sv_types(field_dict):
    """
    SignalVine has it's own types that we'll map over to Python primatives.
    """

    new_dict = {}
    for k, v in field_dict.items():
        print(k, v)

        if "Maybe" in v:
            required = False
        else:
            required = True

        if "Boolean" in v:
            new_type = "bool"
        elif "Numeric" in v:
            new_type = "int"
        elif "Float" in v:
            new_type = "float"
        else:
            # This will sweep in Date too for now. TBD
            new_type = "str"

        new_dict[k] = {"type": new_type, "required": required}

    return new_dict