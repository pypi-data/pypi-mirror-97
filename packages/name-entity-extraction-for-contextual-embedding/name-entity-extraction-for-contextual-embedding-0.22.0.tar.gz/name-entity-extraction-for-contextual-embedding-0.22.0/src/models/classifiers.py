import logging
from logging.config import fileConfig
from os import path

import torch
from torch import nn
from torchcrf import CRF

fileConfig(path.join(path.dirname(__file__), "../resources/log_config.ini"))
logger = logging.getLogger(__name__)


class CNN(nn.Module):
    def __init__(self, zn_size, num_labels):
        super().__init__()
        self.conv1d = nn.Conv1d(zn_size, num_labels, kernel_size=3, padding=1)

    def forward(self, z_n):
        return self.conv1d(z_n.transpose(1, 2)).transpose(2, 1)


class LinearClassifier(nn.Module):
    def __init__(self, zn_size, num_labels):
        super().__init__()
        self.linear = nn.Linear(zn_size, num_labels)

    def forward(self, z_n):
        return self.linear(z_n)


class GRU(nn.Module):
    def __init__(self, zn_size, num_labels):
        super().__init__()
        self.gru = nn.GRU(zn_size, 100, 2, bidirectional=True, batch_first=True)
        self.linear = nn.Linear(100 * 2, num_labels)
        self.crf = CRF(num_labels, batch_first=True)

    def forward(self, z_n):
        gru_out, _ = self.gru(z_n)
        linear_out = self.linear(gru_out)
        pred = torch.zeros_like(linear_out)
        crf_out = self.crf.decode(linear_out)
        pred[
            torch.arange(pred.size(0)).unsqueeze(1), torch.arange(pred.size(1)), crf_out
        ] = 1
        return pred

    def neg_log_likelihood(self, z_n, y_true, pad_id):
        gru_out, _ = self.gru(z_n)
        linear_out = self.linear(gru_out)
        y_true[y_true == -100] = pad_id
        log_likelihood_score = self.crf(linear_out, y_true, reduction="token_mean")
        return log_likelihood_score


def classifier_factory(
    model_name: str, device: torch.device, **parameters
) -> nn.Module:
    if model_name == "linear":
        return LinearClassifier(parameters["zn_size"], parameters["num_labels"]).to(
            device
        )
    elif model_name == "cnn":
        return CNN(parameters["zn_size"], parameters["num_labels"]).to(device)
    elif model_name == "gru":
        return GRU(parameters["zn_size"], parameters["num_labels"]).to(device)
    raise ValueError(logger.error(f"{model_name}: no such model exists !"))
