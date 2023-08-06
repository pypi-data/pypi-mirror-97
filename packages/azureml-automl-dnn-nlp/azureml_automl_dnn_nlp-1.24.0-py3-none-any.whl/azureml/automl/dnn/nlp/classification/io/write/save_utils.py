# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Utility functions to write the final model and checkpoints during training"""

import os
import pickle
import torch

from azureml.automl.dnn.nlp.classification.common.constants import OutputLiterals


def save_vectorizer(label_vectorizer):
    """Save label vectorizer to outputs directory

    :param label_vecotorizer: Fitted vectorizer
    :type label_vecotorizer: CountVectorizer object
    """
    os.makedirs(OutputLiterals.OUTPUT_DIR, exist_ok=True)
    saving_path = os.path.join(OutputLiterals.OUTPUT_DIR, OutputLiterals.VECTORIZER_FILE_NAME)

    # Save the vectorizer
    pickle.dump(label_vectorizer, open(saving_path, "wb"))


def save_model(model):
    """Save a model to outputs directory.

    :param model: Trained model
    :type model: BERTClass
    """
    os.makedirs(OutputLiterals.OUTPUT_DIR, exist_ok=True)
    model_path = os.path.join(OutputLiterals.OUTPUT_DIR, OutputLiterals.MODEL_FILE_NAME)

    # Save the model
    torch.save(model, model_path)


def save_score_script(score_script_dir=None):
    """Save score_script file to outputs directory.

    :param score_script_dir: Path to save location
    :type score_script_dir: string
    """
    if score_script_dir is None:
        score_script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(score_script_dir, OutputLiterals.SCORE_SCRIPT)) as source_file:
        with open(os.path.join(OutputLiterals.OUTPUT_DIR, OutputLiterals.SCORE_SCRIPT), "w") as output_file:
            output_file.write(source_file.read())
