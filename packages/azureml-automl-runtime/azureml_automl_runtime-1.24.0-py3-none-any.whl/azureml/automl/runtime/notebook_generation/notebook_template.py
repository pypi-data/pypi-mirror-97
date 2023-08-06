# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Notebook generation code used to generate Jupyter notebooks from a Jinja2 template."""
from typing import Any, Dict, Set
import functools
import json
import logging

from .. import __version__
from .utilities import escape_json
from azureml._common._error_definition import AzureMLError
from azureml.automl.core.shared._diagnostics.automl_error_definitions import AutoMLInternal
from azureml.automl.core.shared.exceptions import ClientException, ConfigException

import jinja2
from jinja2 import Environment, meta


logger = logging.getLogger(__name__)


class NotebookTemplate:
    """
    Generates notebooks using a Jupyter notebook template.
    """

    def __init__(self, notebook_template: str) -> None:
        """
        Create an instance of a NotebookGenerator.

        :param notebook_template: the Jupyter notebook to use as a template, as a string
        """
        self.template = notebook_template

    @functools.lru_cache(maxsize=1)
    def get_arguments(self) -> Set[str]:
        """
        Retrieve the names of all the arguments needed to generate the notebook.

        :return: a list of all argument names
        """
        notebook = json.loads(self.template)
        env = Environment()
        args = set()  # type: Set[str]

        # Parse the contents of each notebook cell into an AST and scan for jinja2 variables
        for cell in notebook.get("cells", []):
            source = cell.get("source")
            if source:
                if isinstance(source, str):
                    stringified_source = source
                else:
                    stringified_source = "".join(source)
                parsed = env.parse(stringified_source)
                args |= meta.find_undeclared_variables(parsed)
        return args

    def generate_notebook(self, notebook_args: Dict[str, Any]) -> str:
        """
        Generate a notebook from a template using the provided arguments.

        :param notebook_args: a dictionary containing keyword arguments
        :return: a Jupyter notebook as a string
        """
        required_args = self.get_arguments()
        provided_args = set(notebook_args)
        missing_args = required_args - provided_args
        extra_args = provided_args - required_args

        logger.info("Unused arguments: {}".format(extra_args))

        if any(missing_args):
            raise ClientException._with_error(
                AzureMLError.create(
                    AutoMLInternal,
                    target="generate_notebook",
                    error_details="Mismatch between template and provided arguments. Missing arguments: {}".format(
                        missing_args
                    ),
                )
            )

        # Render the notebook template using the given arguments.
        # Arguments need to be escaped since Jupyter notebooks are in JSON format.
        env = Environment(undefined=jinja2.StrictUndefined)
        template = env.from_string(self.template)
        source = template.render(**{k: escape_json(notebook_args[k]) for k in notebook_args})

        # Tag the notebook with the SDK version used to generate it.
        node = json.loads(source)
        if "metadata" not in node:
            node["metadata"] = {}
        node["metadata"]["automl_sdk_version"] = __version__

        return json.dumps(node)
