from torch import nn
from transformers import BertModel


class BertClassifier(nn.Module):

    def __init__(self, dropout=0.4):

        super(BertClassifier, self).__init__()

        self.bert = BertModel.from_pretrained('bert-base-cased')
        self.dropout1 = nn.Dropout(dropout)
        self.linear1 = nn.Linear(768, 256)
        self.dropout2 = nn.Dropout(dropout)
        self.linear2 = nn.Linear(256, 64)
        self.dropout3 = nn.Dropout(dropout)
        self.linear3 = nn.Linear(64, 7)
        self.relu = nn.ReLU()

    def forward(self, input_id, mask):

        _, pooled_output = self.bert(input_ids= input_id, attention_mask=mask, return_dict=False)
        dropout1_output = self.dropout1(pooled_output)
        linear1_output = self.linear1(dropout1_output)
        dropout2_output = self.dropout2(linear1_output)
        linear2_output = self.linear2(dropout2_output)
        dropout3_output = self.dropout3(linear2_output)
        linear3_output = self.linear3(dropout3_output)
        final_layer = self.relu(linear3_output)

        return final_layer