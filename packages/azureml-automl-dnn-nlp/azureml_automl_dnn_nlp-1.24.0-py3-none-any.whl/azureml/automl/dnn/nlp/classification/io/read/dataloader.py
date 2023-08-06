# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Contains dataloader functions for the classification tasks."""

from azureml.core import Dataset as AmlDataset

import logging
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

from azureml.automl.dnn.nlp.classification.io.read.pytorch_dataset_wrapper import PyTorchDatasetWrapper
from azureml.automl.dnn.nlp.classification.common.constants import DatasetLiterals
from azureml.automl.dnn.nlp.classification.io.write.save_utils import save_vectorizer


_logger = logging.getLogger(__name__)


def convert_dataset_format(train_df, val_df):
    """Converting dataset format for consumption during model training.

    :param train_df: Training DataFrame
    :type train_df: pd.DataFrame
    :param val_df: Validation DataFrame
    :type val_df: pd.DataFrame
    :return: training df, validation df, number of label columns
    :rtype: pd.DataFrame, pd.DataFrame, int
    """
    # Combine both dataframes
    combined_df = pd.concat([train_df, val_df])

    # Get combined label column
    combined_label_col = np.array(combined_df[DatasetLiterals.LABEL_COLUMN].astype(str))

    # TODO: CountVectorizer could run into memory issues for large datasets
    vectorizer = CountVectorizer()
    vectorizer.fit(combined_label_col)
    save_vectorizer(vectorizer)

    train_label_col = np.array(train_df[DatasetLiterals.LABEL_COLUMN].astype(str))
    val_label_col = np.array(val_df[DatasetLiterals.LABEL_COLUMN].astype(str))

    train_count_array = vectorizer.transform(train_label_col)
    val_count_array = vectorizer.transform(val_label_col)

    # Create dataframes with label columns
    train_labels_df = pd.DataFrame(train_count_array.toarray().astype(float))
    train_labels_df.columns = vectorizer.get_feature_names()

    val_labels_df = pd.DataFrame(val_count_array.toarray().astype(float))
    val_labels_df.columns = vectorizer.get_feature_names()

    # Create result dataframe by concatenating text with label dataframe
    train_res_df = pd.concat([train_df[DatasetLiterals.TEXT_COLUMN], train_labels_df], join='outer', axis=1)
    val_res_df = pd.concat([val_df[DatasetLiterals.TEXT_COLUMN], val_labels_df], join='outer', axis=1)

    num_label_cols = len(train_res_df.columns) - 1
    _logger.info("Number of label columns is: {}".format(num_label_cols))
    _logger.info("Train Dataframe obtained has columns: {}".format(train_res_df.columns))
    _logger.info("Train Dataframe has shape: {}".format(train_res_df.shape))

    t_df = train_res_df
    t_df['list'] = train_res_df[train_res_df.columns[1:]].values.tolist()
    t_df = t_df[[DatasetLiterals.TEXT_COLUMN, 'list']].copy()

    v_df = val_res_df
    v_df['list'] = val_res_df[val_res_df.columns[1:]].values.tolist()
    v_df = v_df[[DatasetLiterals.TEXT_COLUMN, 'list']].copy()

    return t_df, v_df, num_label_cols


def dataset_loader(dataset_id, validation_dataset_id, workspace):
    """Save checkpoint to outputs directory.

    :param dataset_id: Unique identifier to fetch dataset from datastore
    :type dataset_id: string
    :param validation_dataset_id: Unique identifier to fetch validation dataset from datastore
    :type validation_dataset_id: string
    :param workspace: workspace where dataset is stored in blob
    :type workspace: Workspace
    :return: training dataset, test datasets, number of label columns
    :rtype: PyTorchDatasetWrapper, PyTorchDatasetWrapper, int
    """

    # Get Training Dataset object
    train_ds = AmlDataset.get_by_id(workspace, dataset_id)
    _logger.info("Type of Dataset is: {}".format(type(train_ds)))

    # Get Validation Dataset object
    validation_ds = AmlDataset.get_by_id(workspace, validation_dataset_id)
    _logger.info("Type of Validation Dataset is: {}".format(type(validation_ds)))

    # Convert Dataset to Dataframe and convert to format required by model
    train_df = train_ds.to_pandas_dataframe()
    validation_df = validation_ds.to_pandas_dataframe()

    t_df, v_df, num_label_cols = convert_dataset_format(train_df, validation_df)

    _logger.info("TRAIN Dataset: {}".format(t_df.shape))
    _logger.info("VALIDATION Dataset: {}".format(v_df.shape))

    training_set = PyTorchDatasetWrapper(t_df)
    validation_set = PyTorchDatasetWrapper(v_df)

    return training_set, validation_set, num_label_cols
