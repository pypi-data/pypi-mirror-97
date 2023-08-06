# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Utility functions used during notebook generation."""
from typing import Any
import json


def escape_json(input_str: Any) -> Any:
    """
    JSON escape a string. Other types are unaffected.

    :param input_str: the string
    :return: an escaped string, or original object if not a string
    """
    if not isinstance(input_str, str):
        return input_str
    return json.dumps(input_str).replace('/', r'\/')[1:-1]
