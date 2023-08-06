# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Scoring functions that can load a serialized model and predict."""

import os
import logging
import torch
import pickle
import numpy as np
import pandas as pd

from torch.utils.data import DataLoader
from azureml.core.experiment import Experiment
from azureml.core import Dataset as AmlDataset
from azureml.automl.dnn.nlp.classification.common.constants import (
    MultiLabelParameters,
    OutputLiterals,
    DatasetLiterals
)
from azureml.core.run import Run
from azureml.automl.dnn.nlp.classification.io.read.pytorch_dataset_wrapper import PyTorchDatasetWrapper


logger = logging.getLogger(__name__)


def _distill_run_from_experiment(run_id, experiment_name=None):
    """Get a Run object

    :param run_id: run id of the run that produced the model
    :type run_id: str
    :param experiment_name: name of experiment that contained the run id
    :type experiment_name: str
    :return: Run object
    :rtype: Run
    """
    current_experiment = Run.get_context().experiment
    experiment = current_experiment

    if experiment_name is not None:
        workspace = current_experiment.workspace
        experiment = Experiment(workspace, experiment_name)

    return Run(experiment=experiment, run_id=run_id)


def load_model_and_vectorizer(run_id, experiment_name=None, artifacts_dir=None):
    """
    :param run_id: run id of the run that produced the model
    :type run_id: str
    :param experiment_name: name of experiment that contained the run id
    :type experiment_name: str
    :param artifacts_dir: artifacts directory
    :type artifacts_dir: str
    :return: InferenceModelWrapper object
    :rtype: inference.InferenceModelWrapper
    """
    logger.info("Start fetching model from artifacts")

    if artifacts_dir is None:
        artifacts_dir = OutputLiterals.OUTPUT_DIR

    run = _distill_run_from_experiment(run_id, experiment_name)

    run.download_file(os.path.join(artifacts_dir, OutputLiterals.MODEL_FILE_NAME),
                      output_file_path=OutputLiterals.MODEL_FILE_NAME)
    logger.info("Finished downloading model from outputs")

    run.download_file(os.path.join(artifacts_dir, OutputLiterals.VECTORIZER_FILE_NAME),
                      output_file_path=OutputLiterals.VECTORIZER_FILE_NAME)
    logger.info("Finished downloading vectorizer from outputs")

    model = torch.load(OutputLiterals.MODEL_FILE_NAME)

    vectorizer = pickle.load(open(OutputLiterals.VECTORIZER_FILE_NAME, "rb"))

    return model, vectorizer


def score(run_id, device, experiment_name=None, output_file=None,
          batch_size=MultiLabelParameters.VALID_BATCH_SIZE,
          input_dataset_id=None, log_output_file_info=False):
    """Generate predictions from input files.

    :param run_id: azureml run id
    :type run_id: str
    :param device: device to be used for inferencing
    :type device: str
    :param experiment_name: name of experiment
    :type experiment_name: str
    :param output_file: path to output file
    :type output_file: str
    :param batch_size: batch size for prediction
    :type batch_size: int
    :param input_dataset_id: The input dataset id.  If this is specified image_list_file is not required.
    :type input_dataset_id: str
    :param log_output_file_info: flag on whether to log output file debug info
    :type log_output_file_info: bool
    """
    logger.info("[start inference: batch_size: {}]".format(batch_size))
    model, vectorizer = load_model_and_vectorizer(run_id, experiment_name=experiment_name)
    logger.info("Model and vectorizer restored successfully")

    run = Run.get_context()
    workspace = run.experiment.workspace

    # Get Validation Dataset object
    ds = AmlDataset.get_by_id(workspace, input_dataset_id)
    logger.info("Type of input Dataset is: {}".format(type(ds)))

    df = ds.to_pandas_dataframe()
    logger.info("Shape of dataframe is: {}".format(df.shape))

    label_columns = vectorizer.get_feature_names()

    target_list = [0.0] * len(label_columns)

    i_df = df[[DatasetLiterals.TEXT_COLUMN]].copy()
    i_df['list'] = [target_list for i in i_df.index]

    inference_set = PyTorchDatasetWrapper(i_df)
    inference_data_loader = DataLoader(inference_set, batch_size=batch_size)

    model.eval()

    fin_outputs = []

    with torch.no_grad():
        for _, data in enumerate(inference_data_loader, 0):
            ids = data['ids'].to(device, dtype=torch.long)
            mask = data['mask'].to(device, dtype=torch.long)
            token_type_ids = data['token_type_ids'].to(device, dtype=torch.long)
            outputs = model(ids, mask, token_type_ids)
            fin_outputs.extend(torch.sigmoid(outputs).cpu().detach().numpy().tolist())

    # Create dataframes with label columns
    predicted_labels_df = pd.DataFrame(np.array([np.array(xi) for xi in fin_outputs]))
    predicted_labels_df.columns = label_columns

    predicted_df = pd.concat([i_df[DatasetLiterals.TEXT_COLUMN], predicted_labels_df], join='outer', axis=1)

    os.makedirs(OutputLiterals.OUTPUT_DIR, exist_ok=True)
    predictions_path = os.path.join(OutputLiterals.OUTPUT_DIR, "predictions.csv")

    predicted_df.to_csv(predictions_path)

    logger.info("Results saved at location: {}".format(predictions_path))

    return
