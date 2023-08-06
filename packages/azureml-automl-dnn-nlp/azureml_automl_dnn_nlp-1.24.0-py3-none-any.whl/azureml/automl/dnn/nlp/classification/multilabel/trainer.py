# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Script with the training for multi-label classification."""

import logging
import numpy as np
from sklearn import metrics
import time
import torch

from azureml.automl.dnn.nlp.classification.common.constants import MultiLabelParameters
from azureml.automl.dnn.nlp.classification.io.write.save_utils import save_model, save_score_script
from azureml.automl.dnn.nlp.classification.multilabel.bert_class import BERTClass


_logger = logging.getLogger(__name__)


def train(model, optimizer, training_loader, epoch, device):
    """Definition of the train function.

    :param model: Pretrained DNN model that needs be fine-tuned for task
    :type model: BERTClass
    :param optimizer: Optimizer for neural network
    :type optimizer: torch.optim.Adam
    :param training_loader: Object for loading training dataset
    :type training_loader: DataLoader
    :param epoch: Number of epochs for training
    :type epoch: int
    :param device: 'cuda' or 'cpu'
    :type device: string
    :return: Trained model
    :rtype: BERTClass
    """
    model.train()
    for _, data in enumerate(training_loader, 0):
        ids = data['ids'].to(device, dtype=torch.long)
        mask = data['mask'].to(device, dtype=torch.long)
        token_type_ids = data['token_type_ids'].to(device, dtype=torch.long)
        targets = data['targets'].to(device, dtype=torch.float)

        outputs = model(ids, mask, token_type_ids)

        optimizer.zero_grad()
        loss = torch.nn.BCEWithLogitsLoss()(outputs, targets)
        if _ % MultiLabelParameters.OUTPUT_EPOCHS_COUNT == 0:
            _logger.info('Epoch: {}, Loss:  {}'.format(epoch, loss.item()))

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    return model


def validation(model, validation_loader, device):
    """Definition of the validation function.

    :param model: Trained model
    :type model: BERTClass
    :param validation_loader: Object for loading validation dataset
    :type validation_loader: DataLoader
    :param device: 'cuda' or 'cpu'
    :type device: string
    :return: final outputs and final targets
    :rtype: List[float], List[float]
    """
    model.eval()
    fin_targets = []
    fin_outputs = []
    with torch.no_grad():
        for _, data in enumerate(validation_loader, 0):
            ids = data['ids'].to(device, dtype=torch.long)
            mask = data['mask'].to(device, dtype=torch.long)
            token_type_ids = data['token_type_ids'].to(device, dtype=torch.long)
            targets = data['targets'].to(device, dtype=torch.float)
            outputs = model(ids, mask, token_type_ids)
            fin_targets.extend(targets.cpu().detach().numpy().tolist())
            fin_outputs.extend(torch.sigmoid(outputs).cpu().detach().numpy().tolist())
    return fin_outputs, fin_targets


def driver(automl_settings, run, device, training_loader, validation_loader, num_label_cols):
    """The main driver function for text multi-label classification tasks

    :param automl_settings: automl_settings parameters
    :type automl_settings: dict
    :param run: Run object
    :type run: azureml.core.run
    :param device: 'cuda' or 'cpu'
    :type device: string
    :param training_loader: for loading training data
    :type training_loader: DataLoader
    :param validation_loader: for loading validation data
    :type validation_loader: DataLoader
    :param num_label_cols: number of label columns
    :type num_label_cols: int
    """
    model = BERTClass(num_label_cols)
    model.to(device)

    # Select optimizer
    optimizer = torch.optim.Adam(params=model.parameters(), lr=MultiLabelParameters.LEARNING_RATE)

    start_time = time.time()
    for epoch in range(MultiLabelParameters.EPOCHS):
        model = train(model, optimizer, training_loader, epoch, device)
        _logger.info("Time for epoch {}: {}".format(epoch, time.time() - start_time))
    _logger.info("Total training time : {}".format(time.time() - start_time))

    start_time = time.time()
    outputs, targets = validation(model, validation_loader, device)
    outputs = np.array(outputs) >= 0.5
    accuracy = metrics.accuracy_score(targets, outputs)
    f1_score_micro = metrics.f1_score(targets, outputs, average='micro')
    f1_score_macro = metrics.f1_score(targets, outputs, average='macro')

    _logger.info("Total validation time : ".format(time.time() - start_time))
    _logger.info("Accuracy: {}".format(accuracy))
    _logger.info("F1 Score (Micro): {}".format(f1_score_micro))
    _logger.info("F1 Score (Macro): {}".format(f1_score_macro))

    # Log metrics
    run.log('accuracy', accuracy)
    run.log('f1_score_micro', f1_score_micro)
    run.log('f1_score_macro', f1_score_macro)

    save_model(model)
    save_score_script()
