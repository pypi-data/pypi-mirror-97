# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Utility methods for interacting with AutoMLPipelineBuilder."""

from typing import Dict

from .exceptions import ConflictingTimeoutException


def _validate_run_config_train(automl_settings: Dict[str, str],
                               compute,
                               node_count,
                               process_count_per_node,
                               run_invocation_timeout: int,  # in seconds
                               partition_column_names,
                               input_dataset):
    """
        Validation run config that is passed for training

        This method will validate the configuration to make sure we catch any errors before starting the run.

        :param automl_settings: AutoML configuration settings to be used for triggering AutoML runs during training.
        :param compute: The compute target name or compute target to be used by the pipeline's steps.
        :param node_count: The number of nodes to be used by the pipeline steps when work is
            distributable. This should be less than or equal to the max_nodes of the compute target
            if using amlcompute.
        :param process_count_per_node: The number of processes to use per node when the work is
            distributable. This should be less than or equal to the number of cores of the
            compute target.
        :param run_invocation_timeout: Specifies timeout for each AutoML run.
        :param partition_column_names: Column names which are used to partition the input data.
        :param input_dataset: The input dataset that is used.
    """

    experiment_timeout_hours = int(automl_settings.get('experiment_timeout_hours', 0))
    if run_invocation_timeout <= experiment_timeout_hours * 60 * 60:
        error_msg = ("run_invocation_timeout (in seconds) should be greater than experiment_timeout_hours. "
                     "The run_invocation_timeout (in seconds) should be set to maximum training time of "
                     "one AutoML run with some buffer).")
        raise ConflictingTimeoutException(error_msg)
