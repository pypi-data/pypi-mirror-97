# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
Contains functionality for building pipelines using AutoML for advanced model building.
"""
import json
import os
import pathlib
import shutil
from typing import Any, Dict, List, Optional, Union

from azureml._base_sdk_common._docstring_wrapper import experimental
from azureml._common._error_definition import AzureMLError
from azureml._restclient.jasmine_client import JasmineClient

from azureml.automl.core.shared._diagnostics.automl_error_definitions import ExecutionFailure
from azureml.automl.core.shared.exceptions import ValidationException
from azureml.core import ComputeTarget, Datastore, Environment, Experiment
from azureml.data.data_reference import DataReference
from azureml.pipeline.core import PipelineData, PipelineRun, PipelineStep
from azureml.pipeline.steps import ParallelRunConfig, ParallelRunStep

from ._assets import many_models_inference_driver, many_models_train_driver
from . import utilities

AUTOML_CURATED_ENV_SCENARIO = "AutoML"
MAX_AUTOML_RUN_CONCURRENCY = 320

PROJECT_DIR = "automl_project_dir"
MANY_MODELS_TRAIN_STEP_RUN_NAME = "many-models-train"


@experimental
class AutoMLPipelineBuilder:
    """
    Pipeline builder class.

    This class is used to build pipelines for AutoML training utilizing advanced modeling
    techniques including many models and hierarchical time series.
    """
    @staticmethod
    def get_many_models_train_steps(
        experiment: Experiment,
        automl_settings: Dict[str, Any],
        train_data: DataReference,
        compute_target: Union[str, ComputeTarget],
        partition_column_names: List[str],
        node_count: int,
        process_count_per_node: int = 2,
        run_invocation_timeout: int = 3700,
        output_datastore: Optional[Datastore] = None,
        train_env: Optional[str] = None,
        arguments: Optional[List[Union[str, int]]] = None
    ) -> List[PipelineStep]:
        """
        Get the pipeline steps AutoML many models training.

        This method will build a list of steps to be used for training using AutoML many model scenario
        using ParallelRunStep.

        :param experiment: Experiment object.
        :param automl_settings: AutoML configuration settings to be used for triggering AutoML runs during training.
        :param train_data: The data to be used for training.
        :param compute_target: The compute target name or compute target to be used by the pipeline's steps.
        :param partition_column_names: Column names which are used to partition the input data.
        :param node_count: The number of nodes to be used by the pipeline steps when work is
            distributable. This should be less than or equal to the max_nodes of the compute target
            if using amlcompute.
        :param process_count_per_node: The number of processes to use per node when the work is
            distributable. This should be less than or equal to the number of cores of the
            compute target.
        :param run_invocation_timeout: Specifies timeout for each AutoML run.
        :param output_datastore: The datastore to be used for output. If specified any pipeline
            output will be written to that location. If unspecified the default datastore will be used.
        :param train_env: Specifies the environment definition to use for training. If none specified latest
            curated environment would be used.
        :param arguments: Arguments to be passed to training script.
        :returns: A list of steps which will preprocess data to the desired training_level (as set in
            the automl_settings) and train and register automl models.
        """

        AutoMLPipelineBuilder._clean_project_dir()

        training_output_name = "many_models_training_output"

        output_dir = PipelineData(name=training_output_name,
                                  datastore=output_datastore)

        parallel_run_config = AutoMLPipelineBuilder._build_parallel_run_config_train(experiment,
                                                                                     automl_settings,
                                                                                     compute_target,
                                                                                     node_count,
                                                                                     process_count_per_node,
                                                                                     run_invocation_timeout,
                                                                                     partition_column_names,
                                                                                     train_data,
                                                                                     train_env)

        arguments = [] if arguments is None else arguments
        arguments.append("--node_count")
        arguments.append(node_count)
        parallel_run_step = ParallelRunStep(
            name=MANY_MODELS_TRAIN_STEP_RUN_NAME,
            parallel_run_config=parallel_run_config,
            allow_reuse=False,
            inputs=[train_data],
            output=output_dir,
            arguments=arguments
        )

        return [parallel_run_step]

    @staticmethod
    def get_many_models_batch_inference_steps(
        experiment: Experiment,
        inference_data: DataReference,
        compute_target: Union[str, ComputeTarget],
        partition_column_names: List[str],
        node_count: int,
        process_count_per_node: int = 2,
        run_invocation_timeout: int = 3700,
        mini_batch_size=10,
        output_datastore: Optional[Datastore] = None,
        train_run_id: Optional[str] = None,
        train_experiment_name: Optional[str] = None,
        inference_env: Optional[Environment] = None,
        time_column_name: Optional[str] = None,
        target_column_name: Optional[str] = None,
        arguments: Optional[List[str]] = None
    ) -> List[PipelineStep]:
        """
        Get the pipeline steps AutoML many models inferencing.

        This method will build a list of steps to be used for training using AutoML many model scenario
        using ParallelRunStep.

        :param experiment: Experiment object.
        :param inference_data: The data to be used for training.
        :param compute_target: The compute target name or compute target to be used by the pipeline's steps.
        :param partition_column_names: Partition column names.
        :param node_count: The number of nodes to be used by the pipeline steps when work is
            distributable. This should be less than or equal to the max_nodes of the compute target
            if using amlcompute.
        :param process_count_per_node: The number of processes to use per node when the work is
            distributable. This should be less than or equal to the number of cores of the
            compute target.
        :param run_invocation_timeout: Specifies timeout for inferencing batch.
        :param mini_batch_size: Mini batch size, indicates how many batches will be processed by one process
            on the compute.
        :param output_datastore: The datastore to be used for output. If specified any pipeline
            output will be written to that location. If unspecified the default datastore will be used.
        :param train_run_id: Training run id, which will be used to fetch the right environment for inferencing.
        :param train_experiment_name: Training experiment name, , which will be used to fetch the right
            environment for inferencing.
        :param inference_env: Specifies the environment definition to use for training. If none specified latest
            curated environment would be used.
        :param time_column_name: Optional parameter, used for timeseries
        :param target_column_name:  Needs to be passed only if inference data contains target column.
        :param arguments: Arguments to be passed to training script.
        :returns: A list of steps which will do batch inference using the inference data,
        """

        if inference_env is None and (train_run_id is None or train_experiment_name is None):
            raise Exception("Either pass inference_env or pass train_run_id and train_experiment_name")

        parallel_run_config = AutoMLPipelineBuilder.\
            _build_parallel_run_config_inference(experiment=experiment,
                                                 train_run_id=train_run_id,
                                                 train_experiment_name=train_experiment_name,
                                                 inference_env=inference_env,
                                                 compute_target=compute_target,
                                                 node_count=node_count,
                                                 process_count_per_node=process_count_per_node,
                                                 run_invocation_timeout=run_invocation_timeout,
                                                 mini_batch_size=mini_batch_size)

        inference_output_name = 'many_models_inference_output'

        output_dir = PipelineData(name=inference_output_name,
                                  datastore=output_datastore)

        arguments = [] if arguments is None else arguments
        # Note that partition_column_names is reserved keyword by PRS
        arguments.append('--partition_column_names')
        arguments.extend(partition_column_names)
        if time_column_name:
            arguments.append('--time_column_name')
            arguments.append(time_column_name)
        if target_column_name:
            arguments.append('--target_column_name')
            arguments.append(target_column_name)
        parallel_run_step = ParallelRunStep(
            name="many-models-inference",
            parallel_run_config=parallel_run_config,
            inputs=[inference_data],
            output=output_dir,
            arguments=arguments)
        return [parallel_run_step]

    @ staticmethod
    def _validate_max_concurrency(
            node_count: int,
            process_count_per_node: int,
            jasmine_client: JasmineClient):
        max_concurrent_runs = node_count * process_count_per_node
        try:
            validation_output = jasmine_client.validate_many_models_run(max_concurrent_runs=max_concurrent_runs)
            validation_results = validation_output.response
            if not validation_output.is_valid and any([d.code != "UpstreamSystem"
                                                       for d in validation_results.error.details]):
                # If validation service meets error thrown by the upstream service, the run will continue.
                print("The validation results are as follows:")
                errors = []
                for result in validation_results.error.details:
                    if result.code != "UpstreamSystem":
                        print(result.message)
                        errors.append(result.message)
                msg = "Validation error(s): {}".format(validation_results.error.details)
                raise ValidationException._with_error(AzureMLError.create(
                    ExecutionFailure, operation_name="data/settings validation", error_details=msg)
                )
        except Exception as e:
            # we will get exception when JOS changes are not deployed for the new API
            if max_concurrent_runs > MAX_AUTOML_RUN_CONCURRENCY:
                print("Please decrease concurrency to maximum of {} as currently AutoML does not support it.".format(
                    MAX_AUTOML_RUN_CONCURRENCY))
                raise ValueError("node_count * process_count_per_node must be between 1 and max_concurrency: {}"
                                 .format(MAX_AUTOML_RUN_CONCURRENCY))

    @ staticmethod
    def _write_automl_settings_to_file(automl_settings: Dict[str, str]):
        with open('{}//automl_settings.json'.format(PROJECT_DIR), 'w', encoding='utf-8') as f:
            json.dump(automl_settings, f, ensure_ascii=False, indent=4)

    @ staticmethod
    def _clean_project_dir():
        project_dir = pathlib.Path(PROJECT_DIR)
        if not project_dir.exists():
            project_dir.mkdir()
        else:
            try:
                files = project_dir.glob("*")
                for f in files:
                    os.remove(f)
            except Exception as e:
                print("Warning: Could not clean {} directory. {}".format(PROJECT_DIR, e))
                pass

    @ staticmethod
    def _build_parallel_run_config_train(
            experiment,
            automl_settings: Dict[str, str],
            compute,
            node_count,
            process_count_per_node,
            run_invocation_timeout,
            partition_column_names,
            input_dataset,
            train_env: Environment):

        jasmine_client = JasmineClient(service_context=experiment.workspace.service_context,
                                       experiment_name=experiment.name,
                                       experiment_id=experiment.id)
        AutoMLPipelineBuilder._validate_max_concurrency(node_count, process_count_per_node, jasmine_client)

        AutoMLPipelineBuilder._write_automl_settings_to_file(automl_settings)
        utilities._validate_run_config_train(automl_settings, compute, node_count, process_count_per_node,
                                             run_invocation_timeout, partition_column_names, input_dataset)

        if train_env is None:
            enable_dnn = automl_settings.get("enable_dnn", False)
            # GPU based learners are currently available only for remote runs and so not available for many model runs
            enable_gpu = automl_settings.get("enable_gpu", False)
            train_env = jasmine_client.get_curated_environment(AUTOML_CURATED_ENV_SCENARIO,
                                                               enable_dnn,
                                                               enable_gpu,
                                                               compute)

        # copy the driver script.
        train_driver_path = pathlib.Path(many_models_train_driver.__file__).absolute()
        shutil.copyfile(train_driver_path, os.path.join("{}/{}".format(PROJECT_DIR, train_driver_path.name)))

        dataset_type = str(type(input_dataset))
        parallel_run_config = None
        # TODO: Merge these two in better fashion once tabular dataset is released to public.
        if(dataset_type == "<class 'azureml.data.tabular_dataset.TabularDataset'>"):
            parallel_run_config = ParallelRunConfig.create_with_partition_column_names(
                source_directory=PROJECT_DIR,
                entry_script='many_models_train_driver.py',
                partition_keys=partition_column_names,  # do not modify this setting
                run_invocation_timeout=run_invocation_timeout,
                error_threshold=-1,
                output_action="append_row",
                environment=train_env,
                process_count_per_node=process_count_per_node,
                compute_target=compute,
                node_count=node_count)
        else:  # File dataset
            parallel_run_config = ParallelRunConfig(
                source_directory=PROJECT_DIR,
                entry_script='many_models_train_driver.py',
                mini_batch_size="1",  # do not modify this setting
                run_invocation_timeout=run_invocation_timeout,
                error_threshold=-1,
                output_action="append_row",
                environment=train_env,
                process_count_per_node=process_count_per_node,
                compute_target=compute,
                node_count=node_count)

        return parallel_run_config

    @ staticmethod
    def _build_parallel_run_config_inference(experiment,
                                             train_run_id,
                                             train_experiment_name,
                                             inference_env,
                                             compute_target,
                                             node_count,
                                             process_count_per_node,
                                             run_invocation_timeout,
                                             mini_batch_size: int):
        # TODO: this should be user passed or get it from training run.
        if inference_env is None:
            experiment = Experiment(experiment.workspace, train_experiment_name)
            pipeline_run = PipelineRun(experiment, train_run_id)
            step_run = pipeline_run.find_step_run(MANY_MODELS_TRAIN_STEP_RUN_NAME)[0]
            inference_env = step_run.get_environment()

        AutoMLPipelineBuilder._clean_project_dir()
        inference_driver_path = pathlib.Path(many_models_inference_driver.__file__).absolute()
        shutil.copyfile(inference_driver_path, os.path.join("{}/{}".format(PROJECT_DIR, inference_driver_path.name)))

        parallel_run_config = ParallelRunConfig(
            source_directory=PROJECT_DIR,
            entry_script=inference_driver_path.name,
            mini_batch_size='1',  # do not modify this setting
            run_invocation_timeout=run_invocation_timeout,
            error_threshold=-1,
            output_action="append_row",
            environment=inference_env,
            process_count_per_node=process_count_per_node,
            compute_target=compute_target,
            node_count=node_count)
        return parallel_run_config
