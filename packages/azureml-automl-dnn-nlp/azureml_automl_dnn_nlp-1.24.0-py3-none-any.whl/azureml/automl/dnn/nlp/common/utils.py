# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Common utilities across tasks."""

import logging
import os
import sys
from typing import Dict, Optional

from azureml.automl.core.shared import log_server
from azureml.automl.core.shared.logging_fields import TELEMETRY_AUTOML_COMPONENT_KEY
from azureml.automl.dnn.nlp.classification.common.constants import LoggingLiterals
from azureml.automl.dnn.nlp.common.constants import SystemSettings
from azureml.core.run import Run, _OfflineRun
from azureml.telemetry import INSTRUMENTATION_KEY, get_diagnostics_collection_info
from azureml.train.automl import constants
from azureml.train.automl._logging import set_run_custom_dimensions
from azureml.train.automl.constants import ComputeTargets, Tasks


logger = logging.getLogger(__name__)


class AzureAutoMLSettingsStub:
    """Stub for AzureAutoMLSettings class to configure logging."""
    is_timeseries = False
    task_type = None
    compute_target = None
    name = None
    subscription_id = None
    region = None
    verbosity = None
    telemetry_verbosity = None
    send_telemetry = None
    azure_service = None


def _set_logging_parameters(task_type: constants.Tasks,
                            settings: Dict,
                            output_dir: Optional[str] = None,
                            azureml_run: Optional[Run] = None):
    """Sets the logging parameters so that we can track all the training runs from
    a given project.

    :param task_type: The task type for the run.
    :type task_type: constants.Tasks
    :param settings: All the settings for this run.
    :type settings: Dict
    :param output_dir: The output directory.
    :type Optional[str]
    :param azureml_run: The run object.
    :type Optional[Run]
    """
    log_server.update_custom_dimensions({LoggingLiterals.TASK_TYPE: task_type})

    if LoggingLiterals.PROJECT_ID in settings:
        project_id = settings[LoggingLiterals.PROJECT_ID]
        log_server.update_custom_dimensions({LoggingLiterals.PROJECT_ID: project_id})

    if LoggingLiterals.VERSION_NUMBER in settings:
        version_number = settings[LoggingLiterals.VERSION_NUMBER]
        log_server.update_custom_dimensions({LoggingLiterals.VERSION_NUMBER: version_number})

    _set_automl_run_custom_dimensions(task_type, output_dir, azureml_run)


def _set_automl_run_custom_dimensions(task_type: Tasks,
                                      output_dir: Optional[str] = None,
                                      azureml_run: Optional[Run] = None):
    if output_dir is None:
        output_dir = SystemSettings.LOG_FOLDER
    os.makedirs(output_dir, exist_ok=True)

    if azureml_run is None:
        azureml_run = Run.get_context()

    name = "not_available_offline"
    subscription_id = "not_available_offline"
    region = "not_available_offline"
    parent_run_id = "not_available_offline"
    child_run_id = "not_available_offline"
    if not isinstance(azureml_run, _OfflineRun):
        # If needed in the future, we can replace with a uuid5 based off the experiment name
        # name = azureml_run.experiment.name
        name = "online_scrubbed_for_compliance"
        subscription_id = azureml_run.experiment.workspace.subscription_id
        region = azureml_run.experiment.workspace.location
        parent_run_id = azureml_run.parent.id if azureml_run.parent is not None else None
        child_run_id = azureml_run.id

    # Build the automl settings expected by the logger
    send_telemetry, level = get_diagnostics_collection_info(component_name=TELEMETRY_AUTOML_COMPONENT_KEY)
    automl_settings = AzureAutoMLSettingsStub
    automl_settings.is_timeseries = False
    automl_settings.task_type = task_type
    automl_settings.compute_target = ComputeTargets.AMLCOMPUTE
    automl_settings.name = name
    automl_settings.subscription_id = subscription_id
    automl_settings.region = region
    automl_settings.telemetry_verbosity = level
    automl_settings.send_telemetry = send_telemetry

    log_server.set_log_file(os.path.join(output_dir, SystemSettings.LOG_FILENAME))
    if send_telemetry:
        log_server.enable_telemetry(INSTRUMENTATION_KEY)
    log_server.set_verbosity(level)

    set_run_custom_dimensions(
        automl_settings=automl_settings,
        parent_run_id=parent_run_id,
        child_run_id=child_run_id)

    # Add console handler
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    log_server.add_handler('stdout', stdout_handler)
