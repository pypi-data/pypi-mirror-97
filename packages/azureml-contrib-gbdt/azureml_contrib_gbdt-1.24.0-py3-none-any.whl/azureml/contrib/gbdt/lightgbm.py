# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Contains an estimator for training with LightGBM."""

import logging

from azureml.core._experiment_method import experiment_method
from azureml.train._estimator_helper import _estimator_submit_method
from azureml.train.estimator._framework_base_estimator import _FrameworkBaseEstimator
from azureml.core import ScriptRunConfig, Experiment
from azureml.core.compute import AmlCompute
from azureml.exceptions import TrainingException
import os
import shutil


class LightGBM(_FrameworkBaseEstimator):
    """
    Represents an estimator for training in LightGBM.

    Supported versions: 2.2.3

    .. remarks::

            When submitting a training job, Azure ML runs your script in a conda environment within
            a Docker container. LightGBM containers have the following dependencies installed.

            | Dependencies | LightGBM 2.2.3 |
            | ---------------------------- | ----------------- |
            | Python                       | 3.6.2             |
            | azureml-defaults             | Latest            |
            | OpenMpi                      | 3.1.2             |
            | numpy                        | 1.15.4            |
            | scipy                        | 1.1.0             |
            | scikit-learn                 | 0.20.1            |

            The Docker images extend Ubuntu 16.04.

            To install additional dependencies, you can either use the ``pip_packages`` or ``conda_packages``
            parameter. Or, you can specify the ``pip_requirements_file`` or ``conda_dependencies_file`` parameter.
            Alternatively, you can build your own image, and pass the ``custom_docker_image`` parameter to the
            estimator constructor.

            For more information about Docker containers used in LightGBM training, see
            https://github.com/Azure/AzureML-Containers.

    :param source_directory: A local directory containing experiment configuration files.
    :type source_directory: str
    :param compute_target: The compute target where training will happen. This can either be an object or the
        string "local".
    :type compute_target: azureml.core.compute_target.AbstractComputeTarget or str
    :param vm_size: The VM size of the compute target that will be created for the training. Supported values:
        Any `Azure VM size
        <https://docs.microsoft.com/azure/cloud-services/cloud-services-sizes-specs>`_.
    :type vm_size: str
    :param vm_priority: The VM priority of the compute target that will be created for the training. If not
        specified, 'dedicated' is used.

        Supported values:'dedicated' and 'lowpriority'.

        This takes effect only when the ``vm_size param`` is specified in the input.
    :type vm_priority: str
    :param node_count: The number of nodes in the compute target used for training. Only the
        :class:`azureml.core.compute.AmlCompute` target is supported for distributed training (``node_count`` > 1).
    :type node_count: int
    :param distributed_training: Parameters for running a distributed training job.

        For running a distributed job with MPI backend, use :class:`azureml.train.dnn.Mpi`
        object to specify ``process_count_per_node``.
    :type distributed_training: azureml.train.dnn.ParameterServer or
        azureml.train.dnn.Mpi
    :param inputs: A list of azureml.data.data_reference.DataReference objects to use as input.
    :type inputs: list
    :param source_directory_data_store: The backing datastore for project share.
    :type source_directory_data_store: str
    :param shm_size: The size of the Docker container's shared memory block. If not set, default is
        azureml.core.environment._DEFAULT_SHM_SIZE. For more information, see
    `Docker run reference <https://docs.docker.com/engine/reference/run/>`_.
    :type shm_size: str
    :param resume_from: The data path containing the checkpoint or model files from which to resume the experiment.
    :type resume_from: azureml.data.datapath.DataPath
    :param max_run_duration_seconds: The maximum allowed time for the run. Azure ML will attempt to automatically
        cancel the run if it takes longer than this value.
    :type max_run_duration_seconds: int
    :param framework_version: The LightGBM version to be used for executing training code.
        If no version is provided, the estimator will default to the latest version supported by Azure ML.
        Use `LightGBM.get_supported_versions()` to return a list to get a list of all versions supported
        the current Azure ML SDK.
    :type framework_version: str
    :param _enable_optimized_mode: Enable incremental environment build with pre-built framework images for faster
        environment preparation. A pre-built framework image is built on top of Azure ML default CPU/GPU base
        images with framework dependencies pre-installed.
    :type _enable_optimized_mode: bool
    if environment_definition is not None and environment_definition.docker.gpu_support:
        logging.warning("The LightGBM estimator does not have GPU support yet. Use CPU for now instead.")
        environment_definition.docker.gpu_support = False
    :param lightgbm_config: path of lightgbm config file
    :type lightgbm_config: str
    :param task: type of task: train, predict, convert_model, and refit. Default to train.
    :type task: str
    :param objective: objective of training. Default to regression.
    :type objective: str
    :param boosting: choose the type of boosting method to use: gbdt, rf, dart, goss. Default to gbdt.
    :type boosting: str
    :param data: file location for training data for each rank
    :type data: list
    :param valid: file location for test/validation data for each rank
    :type valid: list
    :param num_iterations: number of iterations
    :type num_iterations: int
    :param learning_rate: learning rate
    :type learning_rate: float
    :param num_leaves: number of leaves
    :type num_leaves: int
    :param tree_learner: type of tree learner
    :type tree_learner: str
    :param num_threads: number of threads for LightGBM
    :type num_threads: int
    :param seed: this seed is used to generate other seeds
    :type seed: int
    :param kwargs: this keyword pair is used to pass other parameters that LightGBM CLI accepts
    Exposing core parameters according to https://lightgbm.readthedocs.io/en/latest/Parameters.html,
    other parameters can be passed with **kwargs
    :type kwargs: dictionary
    """

    FRAMEWORK_NAME = "LightGBM"
    DEFAULT_VERSION = "2.2.3"
    _SUPPORTED_BACKENDS = ["mpi"]

    @experiment_method(submit_function=_estimator_submit_method)
    def __init__(self,
                 source_directory,
                 *,
                 compute_target=None,
                 vm_size=None,
                 vm_priority=None,
                 node_count=1,
                 distributed_training=None,
                 inputs=None,
                 source_directory_data_store=None,
                 shm_size=None,
                 resume_from=None,
                 max_run_duration_seconds=None,
                 framework_version=DEFAULT_VERSION,
                 _enable_optimized_mode=False,
                 lightgbm_config=None,
                 task=None,
                 objective=None,
                 boosting=None,
                 data=None,
                 valid=None,
                 num_iterations=None,
                 learning_rate=None,
                 num_leaves=None,
                 tree_learner=None,
                 num_threads=None,
                 seed=None,
                 **kwargs
                 ):
        """Initialize a LightGBM estimator.

        Please see https://lightgbm.readthedocs.io/en/latest/Parameters.html for full list of parameters.
        Core parameters are specified here, others can be passed in with key pair values.
        :param source_directory: A local directory containing experiment configuration files.
        :type source_directory: str
        :param compute_target: The compute target where training will happen. This can either be an object or the
            string "local".
        :type compute_target: azureml.core.compute_target.AbstractComputeTarget or str
        :param vm_size: The VM size of the compute target that will be created for the training. Supported values:
            Any `Azure VM size
            <https://docs.microsoft.com/azure/cloud-services/cloud-services-sizes-specs>`_.
        :type vm_size: str
        :param vm_priority: The VM priority of the compute target that will be created for the training. If not
            specified, 'dedicated' is used.

            Supported values:'dedicated' and 'lowpriority'.

            This takes effect only when the ``vm_size param`` is specified in the input.
        :type vm_priority: str
        :param node_count: The number of nodes in the compute target used for training. Only the
            :class:`azureml.core.compute.AmlCompute` target is supported for distributed training (``node_count`` > 1).
        :type node_count: int
        :param distributed_training: Parameters for running a distributed training job.

            For running a distributed job with MPI backend, use :class:`azureml.train.dnn.Mpi`
            object to specify ``process_count_per_node``.
        :type distributed_training: azureml.train.dnn.ParameterServer or
            azureml.train.dnn.Mpi
        :param inputs: A list of azureml.data.data_reference.DataReference objects to use as input.
        :type inputs: list
        :param source_directory_data_store: The backing datastore for project share.
        :type source_directory_data_store: str
        :param shm_size: The size of the Docker container's shared memory block. If not set, default is
            azureml.core.environment._DEFAULT_SHM_SIZE. For more information, see
        `Docker run reference <https://docs.docker.com/engine/reference/run/>`_.
        :type shm_size: str
        :param resume_from: The data path containing the checkpoint or model files from which to resume the experiment.
        :type resume_from: azureml.data.datapath.DataPath
        :param max_run_duration_seconds: The maximum allowed time for the run. Azure ML will attempt to automatically
            cancel the run if it takes longer than this value.
        :type max_run_duration_seconds: int
        :param framework_version: The LightGBM version to be used for executing training code.
            If no version is provided, the estimator will default to the latest version supported by Azure ML.
            Use `LightGBM.get_supported_versions()` to return a list to get a list of all versions supported
            the current Azure ML SDK.
        :type framework_version: str
        :param _enable_optimized_mode: Enable incremental environment build with pre-built framework images for faster
            environment preparation. A pre-built framework image is built on top of Azure ML default CPU/GPU base
            images with framework dependencies pre-installed.
        :type _enable_optimized_mode: bool
        if environment_definition is not None and environment_definition.docker.gpu_support:
            logging.warning("The LightGBM estimator does not have GPU support yet. Use CPU for now instead.")
            environment_definition.docker.gpu_support = False
        :param lightgbm_config: path of lightgbm config file
        :type lightgbm_config: str
        :param task: type of task: train, predict, convert_model, and refit. Default to train.
        :type task: str
        :param objective: objective of training. Default to regression.
        :type objective: str
        :param boosting: choose the type of boosting method to use: gbdt, rf, dart, goss. Default to gbdt.
        :type boosting: str
        :param data: file location for training data for each rank
        :type data: list
        :param valid: file location for test/validation data for each rank
        :type valid: list
        :param num_iterations: number of iterations
        :type num_iterations: int
        :param learning_rate: learning rate
        :type learning_rate: float
        :param num_leaves: number of leaves
        :type num_leaves: int
        :param tree_learner: type of tree learner
        :type tree_learner: str
        :param num_threads: number of threads for LightGBM
        :type num_threads: int
        :param seed: this seed is used to generate other seeds
        :type seed: int
        :param kwargs: this keyword pair is used to pass other parameters that LightGBM CLI accepts
        Exposing core parameters according to https://lightgbm.readthedocs.io/en/latest/Parameters.html,
        other parameters can be passed with **kwargs
        :type kwargs: dictionary
        """
        if node_count > 1 and (len(data) != node_count or len(valid) != node_count):
            logging.warning("number of training file doesn't match number of ranks")
        if not isinstance(compute_target, AmlCompute):
            raise TrainingException("LightGBM only supports AmlCompute compute target.")

        image_name = 'viennaprivate.azurecr.io/lightgbm:2.2.3-cpu'

        super().__init__(source_directory, compute_target=compute_target, vm_size=vm_size,
                         vm_priority=vm_priority,
                         node_count=node_count,
                         distributed_training=distributed_training,
                         use_gpu=False, use_docker=True, custom_docker_image=image_name,
                         inputs=inputs,
                         source_directory_data_store=source_directory_data_store,
                         shm_size=shm_size, resume_from=resume_from,
                         max_run_duration_seconds=max_run_duration_seconds,
                         framework_name=self.FRAMEWORK_NAME,
                         framework_version=framework_version,
                         _enable_optimized_mode=_enable_optimized_mode)

        self._estimator_config.communicator = 'OpenMpi'
        self.lightgbm_config = lightgbm_config
        self.task = task
        self.objective = objective
        self.boosting = boosting
        self.data = data
        self.valid = valid
        self.num_iterations = num_iterations
        self.learning_rate = learning_rate
        self.num_leaves = num_leaves
        self.tree_learner = tree_learner
        self.num_threads = num_threads
        self.seed = seed
        self.kwargs = kwargs

    def _get_args(self):
        arguments = []

        if self.lightgbm_config:
            arguments.append('--train_conf_file')
            arguments.append(str(self.lightgbm_config))

        if self. task:
            arguments.append('--task')
            arguments.append(str(self.task))

        if self.objective:
            arguments.append('--objective')
            arguments.append(str(self.objective))

        if self.boosting:
            arguments.append('--boosting')
            arguments.append(str(self.boosting))

        if self.data:
            arguments.append('--data')
            for train_file in self.data:
                arguments.append(train_file)

        if self.valid:
            arguments.append('--valid')
            for train_file in self.data:
                arguments.append(train_file)

        if self.num_iterations:
            arguments.append('--num_iterations')
            arguments.append(int(self.num_iterations))

        if self.learning_rate:
            arguments.append('--learning_rate')
            arguments.append(float(self.learning_rate))

        if self.num_leaves:
            arguments.append('--num_leaves')
            arguments.append(int(self.num_leaves))

        if self.tree_learner:
            arguments.append('--tree_learner')
            arguments.append(str(self.tree_learner))

        if self.num_threads:
            arguments.append('--num_threads')
            arguments.append(int(self.num_threads))

        if self.seed:
            arguments.append('--seed')
            arguments.append(str(self.seed))

        for key, value in self.kwargs.items():
            arg_name = key
            arguments.append(arg_name)
            arguments.append(value)

        return arguments

    def _fit(self, workspace, experiment_name):
        dir_name = os.path.dirname(__file__)
        file_name = 'run_lgbm.py'
        # copying over run_lgbm.py from python library
        shutil.copy(os.path.join(dir_name, file_name), file_name)
        src = ScriptRunConfig(source_directory='.',
                              script=file_name,
                              arguments=self._get_args(),
                              run_config=self._estimator_config)

        exp = Experiment(workspace, experiment_name)
        run = exp.submit(config=src)
        return run

    def _get_telemetry_values(self, func):
        try:
            telemetry_values = super()._get_telemetry_values(func)
            return telemetry_values
        except:
            pass
