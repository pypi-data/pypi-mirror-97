# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
#
# For BERT and HuggingFace Transformers:
#
# Copyright 2018 The Google AI Language Team Authors and The HuggingFace Inc. team.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# For BERTClass:
#
# MIT License
#
# Copyright (c) 2020 Abhishek Kumar Mishra
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""BERTClass class for constructing neural-net using BERT"""

import torch
import transformers

from azureml.automl.dnn.nlp.classification.common.constants import\
    ModelNames, MultiLabelParameters


class BERTClass(torch.nn.Module):
    """Class for creating the neural network using pretrained BERT.

    Creating the customized model, by adding a drop out and a dense layer on top of BERT
    to get the final output for the model.
    """
    BERT_BASE_HIDDEN_DIM = 768

    def __init__(self, num_label_cols):
        """Init function definition."""
        super(BERTClass, self).__init__()
        self.l1 = transformers.BertModel.from_pretrained(ModelNames.BERT_BASE_UNCASED)
        self.l2 = torch.nn.Dropout(MultiLabelParameters.DROPOUT)
        self.l3 = torch.nn.Linear(self.BERT_BASE_HIDDEN_DIM, num_label_cols)

    def forward(self, ids, mask, token_type_ids):
        """Forward function definition."""
        _, output_1 = self.l1(ids, attention_mask=mask, token_type_ids=token_type_ids)
        output_2 = self.l2(output_1)
        output = self.l3(output_2)
        return output
