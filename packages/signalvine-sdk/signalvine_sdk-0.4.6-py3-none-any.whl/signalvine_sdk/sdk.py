import pandas as pd
import requests
import logging
import json
import time
from signalvine_sdk.common import (
    APIError,
    build_headers,
    convert_participants_to_records,
    convert_sv_types,
    make_body,
)
from typing import List, Dict, Optional, Tuple, Union
from box import Box

LOGGER = logging.getLogger(__name__)


class SignalVineSDK:
    def __init__(
        self,
        account_number: str,
        account_token: str,
        account_secret: str,
        api_hostname: str = "https://theseus-api.signalvine.com",
    ):

        # These are secrets that need to be set in the environment
        self.account_number = account_number
        self.account_token = account_token
        self.account_secret = account_secret
        assert self.account_secret, "Environment variables not set."

        self.api_hostname = api_hostname

    def get_programs(self, include_active: bool = True) -> List:
        """
        Get the program info for a specific account.
        """
        participant_path = f"/v1/accounts/{self.account_number}/programs"

        headers = build_headers(
            self.account_token, self.account_secret, "GET", participant_path
        )

        url = f"{self.api_hostname}{participant_path}"

        if include_active:
            # To ensure we get a list of all programs, not just the active ones.
            url += "?active=all"

        r = requests.get(url, headers=headers)

        if r.status_code == 200:
            return r.json()["items"]
        else:
            raise APIError(r.status_code, f"API reason: {r.text}")

    def get_participants_chunk(
        self,
        program_id: str,
        chunk_size: int = 500,
        offset: int = 0,
        include_active: bool = True,
    ) -> List:
        """
        A helper function that lets us get a page of contacts at a time.
        If used to page, ensure the chunk_size is the same, or the 'pages'
        don't work anymore.

        Returns a list of json records. The column names we're looking for
        are in a field called profile, so we'll straighten that out later.

        This method returns 'raw' participant info, mostly exactly what comes
        from SV.
        """

        participant_path = f"/v1/programs/{program_id}/participants"

        headers = build_headers(
            self.account_token, self.account_secret, "GET", participant_path
        )

        url = f"{self.api_hostname}{participant_path}?type=full&count={chunk_size}&offset={offset}"

        if include_active:
            # Otherwise we only get the active fields
            url += "&active=all"

        r = requests.get(url, headers=headers)

        if r.status_code == 200:
            return r.json()["items"]
        else:
            raise APIError(r.status_code, f"API reason: {r.text}")

    def upsert_participants(
        self,
        program_id: str,
        records_df: pd.DataFrame,
        new_flag: str = "add",
        mode_flag: str = "tx",
    ):
        """
        From https://support.signalvine.com/hc/en-us/articles/360023207353-API-documentation

        It's on you to format the dates correctly in the dataframe.

        Also, this drops duplicates. No quarter. It's mayhem in SV if a phone already exists.

        Mode is 'row' or 'tx'. In tx mode, it's all or nothing.
        """

        # Drop the duplicates... TODO log duplicate numbers
        # records_df = records_df.drop_duplicates(subset=["phone"], keep=False)

        participant_path = f"/v2/programs/{program_id}/participants"

        body = make_body(
            program_id=program_id,
            content_df=records_df,
            new_flag=new_flag,
            mode_flag=mode_flag,
        )

        header_body = json.dumps(body, separators=(",", ":"), sort_keys=False)

        headers = build_headers(
            token=self.account_token,
            secret=self.account_secret,
            action="POST",
            path_no_query=participant_path,
            body=header_body,
        )

        url = f"{self.api_hostname}{participant_path}"
        r = requests.post(url, json=body, headers=headers)

        # Things get funky here. We're looking for a 202, and if so,
        # get a Location from the headers, then GET that (in a loop?!)
        # until we see "complete".

        if r.status_code == 202:
            # return the location path so we can orchestrate it outside of here.
            location_path = r.headers["Location"]
            return location_path
        else:
            raise APIError(r.status_code, f"API reason: {r.text}")

    def get_location_status(self, location_path: str) -> Tuple[bool, str]:
        url = f"{self.api_hostname}{location_path}"

        headers = build_headers(
            token=self.account_token,
            secret=self.account_secret,
            path_no_query=location_path,
        )

        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            status_json = r.json()
            if status_json["complete"] == True:
                # only if this is complete do we care to sift through it.
                if status_json["error"] == True:
                    return True, status_json["message"]
                else:
                    return True, None
            else:
                # not complete; just say so
                return False, None
        else:
            raise APIError(r.status_code, f"API reason: {r.text}")

    def get_program_schema(self, program_id, convert_to_python_types=False) -> Dict:
        """
        Get the schema for the participant records
        Return it as a dictionary in the form {name:type}.
        Type is still the SignalVine type.

        Set convert_to_python_types to True to return Python primative types instead
        """

        schema_path = f"/v1/programs/{program_id}"

        # We build the headers off the path alone without query
        headers = build_headers(
            self.account_token, self.account_secret, "GET", schema_path
        )

        url = f"{self.api_hostname}{schema_path}"

        # We could also just tack these to the end of the url
        params = {"type": "schema"}

        r = requests.get(url, params=params, headers=headers)

        if r.status_code == 200:

            # convert the fields to a dict
            fields_dict = {}
            for item in r.json()["fields"]:
                fields_dict[item["name"]] = item["type"]

            if convert_to_python_types:
                return convert_sv_types(fields_dict)
            else:
                return fields_dict

        else:
            raise APIError(r.status_code, f"API reason: {r.text}")