import unittest
from azureml.automl.dnn.nlp.classification.multilabel.bert_class import BERTClass

try:
    import torch
    has_torch = True
except ImportError:
    has_torch = False


class TestBertClass:
    @unittest.skipIf(not has_torch, "torch not installed")
    def test_bert_class(self):
        NUM_MULTI_LABEL_COL = 4
        INPUT_SIZE = 1000
        model = BERTClass(NUM_MULTI_LABEL_COL)
        input_tensor = torch.randn(INPUT_SIZE, BERTClass.BERT_BASE_HIDDEN_DIM)
        output_tensor = model.l3(input_tensor)
        assert torch.is_tensor(output_tensor)
        assert output_tensor.size() == torch.Size([INPUT_SIZE, NUM_MULTI_LABEL_COL])
