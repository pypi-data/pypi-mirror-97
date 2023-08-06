# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Entry script that is invoked by the driver script from automl."""
import logging
from torch import cuda
from torch.utils.data import DataLoader, RandomSampler

from azureml.automl.dnn.nlp.classification.common.constants import MultiLabelParameters, Warnings
from azureml.automl.dnn.nlp.classification.io.read.dataloader import dataset_loader
from azureml.automl.dnn.nlp.classification.multilabel.trainer import driver
from azureml.core.run import Run
from azureml.train.automl.runtime._entrypoints.utils.common import parse_settings


_logger = logging.getLogger(__name__)


def run(automl_settings):
    """Invoke training by passing settings and write the output model.
    :param automl_settings: dictionary with automl settings
    """
    run = Run.get_context()

    automl_settings_obj = parse_settings(run, automl_settings)
    _logger.info("AutoMLSetting Object: {}".format(automl_settings_obj))

    workspace = run.experiment.workspace

    # is_gpu is False by default
    is_gpu = False

    device = 'cuda' if cuda.is_available() else 'cpu'

    if hasattr(automl_settings_obj, "is_gpu") and automl_settings_obj.is_gpu:
        is_gpu = True

    if is_gpu and device == 'cpu':
        _logger.warning(Warnings.CPU_DEVICE_WARNING)

    # Print device information to logs
    _logger.info("is_gpu is {} device found is {}".format(is_gpu, device))

    # Get training and validation dataset ID from automl_settings
    dataset_id = automl_settings.get('dataset_id', None)
    _logger.info("Training Dataset id is: {}".format(dataset_id))

    validation_dataset_id = automl_settings.get('validation_dataset_id', None)
    _logger.info("Validation Dataset id is: {}".format(validation_dataset_id))

    # Obtain training and test data
    training_set, validation_set, num_label_cols = dataset_loader(dataset_id, validation_dataset_id, workspace)

    train_sampler = RandomSampler(training_set)
    validation_sampler = RandomSampler(validation_set)

    training_loader = DataLoader(training_set, sampler=train_sampler, batch_size=MultiLabelParameters.TRAIN_BATCH_SIZE)
    validation_loader = DataLoader(validation_set, sampler=validation_sampler,
                                   batch_size=MultiLabelParameters.VALID_BATCH_SIZE)

    # Call training script
    driver(automl_settings, run, device, training_loader, validation_loader, num_label_cols)
