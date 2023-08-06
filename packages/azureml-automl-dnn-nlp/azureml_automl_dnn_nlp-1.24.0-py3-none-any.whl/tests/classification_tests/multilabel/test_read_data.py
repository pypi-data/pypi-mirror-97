import pandas as pd
import pytest
import unittest

from azureml.automl.dnn.nlp.classification.common.constants import DatasetLiterals
from azureml.automl.dnn.nlp.classification.io.read.pytorch_dataset_wrapper import PyTorchDatasetWrapper
from azureml.automl.dnn.nlp.classification.io.read.dataloader import convert_dataset_format

try:
    import torch
    has_torch = True
except ImportError:
    has_torch = False


@pytest.mark.usefixtures('get_nlp_data')
class TestPyTorchDatasetWrappert:
    @unittest.skipIf(not has_torch, "torch not installed")
    def test_pytorch_dataset_wrapper(self):
        input_df = pd.read_csv("multilabel/test_dataset.csv", index_col=False)
        training_df, validation_df, num_label_cols = convert_dataset_format(input_df, input_df)
        assert num_label_cols == 6
        training_df['list'] = training_df[training_df.columns[1:]].values.tolist()
        training_df = training_df[[DatasetLiterals.TEXT_COLUMN, 'list']].copy()
        training_set = PyTorchDatasetWrapper(training_df)
        assert len(training_set) == 5
        assert all(item in ['ids', 'mask', 'token_type_ids', 'targets'] for item in training_set[1])
        assert all(torch.is_tensor(value) for key, value in training_set[1].items())

    @unittest.skipIf(not has_torch, "torch not installed")
    def test_convert_dataset_format(self):
        input_df = pd.read_csv("multilabel/test_dataset.csv", index_col=False)
        pre_conv_col_list = [DatasetLiterals.TEXT_COLUMN, DatasetLiterals.LABEL_COLUMN, 'label_confidence',
                             'datapoint_id']
        assert input_df.columns.to_list() == pre_conv_col_list
        training_df, validation_df, num_label_cols = convert_dataset_format(input_df, input_df)
        assert num_label_cols == 6
        post_conv_col_list = [DatasetLiterals.TEXT_COLUMN, 'list']
        assert training_df.columns.to_list() == post_conv_col_list
