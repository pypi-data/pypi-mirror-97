# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Constants for classification tasks."""


class OutputLiterals:
    """Directory and file names for artifacts."""
    MODEL_FILE_NAME = 'model.pt'
    CHECKPOINT_FILE_NAME = 'checkpoint'
    VECTORIZER_FILE_NAME = 'vectorizer.pkl'
    OUTPUT_DIR = './outputs'
    SCORE_SCRIPT = 'score_script.py'


class DatasetLiterals:
    """Key columns for Dataset"""
    TEXT_COLUMN = 'text'
    LABEL_COLUMN = 'labels'


class MultiLabelParameters:
    """Defining key variables that will be used later on in the training"""
    MAX_LEN = 128
    TRAIN_BATCH_SIZE = 16
    VALID_BATCH_SIZE = 8
    EPOCHS = 3
    LEARNING_RATE = 1e-05
    OUTPUT_EPOCHS_COUNT = 5000
    DROPOUT = 0.3


class ModelNames:
    """Currently supported model names."""
    BERT_BASE_UNCASED = "bert-base-uncased"


class ScoringLiterals:
    """String names for scoring settings"""
    RUN_ID = 'run_id'
    EXPERIMENT_NAME = 'experiment_name'
    OUTPUT_FILE = 'output_file'
    ROOT_DIR = 'root_dir'
    BATCH_SIZE = 'batch_size'
    INPUT_DATASET_ID = 'input_dataset_id'
    LOG_OUTPUT_FILE_INFO = 'log_output_file_info'


class LoggingLiterals:
    """Literals that help logging and correlating different training runs."""
    PROJECT_ID = 'project_id'
    VERSION_NUMBER = 'version_number'
    TASK_TYPE = 'task_type'


class Warnings:
    """Warning strings."""
    CPU_DEVICE_WARNING = "The device being used for training is 'cpu'. Training can be slow and may lead to " \
                         "out of memory errors. Please switch to a compute with gpu devices. " \
                         "If you are already running on a compute with gpu devices, please check to make sure " \
                         "your nvidia drivers are compatible with torch version {}."
