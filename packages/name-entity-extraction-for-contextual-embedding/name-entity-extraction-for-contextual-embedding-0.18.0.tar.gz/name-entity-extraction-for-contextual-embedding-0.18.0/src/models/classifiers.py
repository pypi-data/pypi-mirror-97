import logging
from logging.config import fileConfig
from os import path
from torch import nn

fileConfig(path.join(path.dirname(__file__), '../resources/log_config.ini'))
logger = logging.getLogger(__name__)


class CNN(nn.Module):
    def __init__(self, zn_size, num_labels):
        super().__init__()
        self.conv1d = nn.Conv1d(zn_size, num_labels, kernel_size=3, padding=1)

    def forward(self, z_n):
        return self.conv1d(z_n)


class LinearClassifier(nn.Module):
    def __init__(self, zn_size, num_labels):
        super().__init__()
        self.linear = nn.Linear(zn_size, num_labels)

    def forward(self, z_n):
        return self.linear(z_n)


def classifier_factory(model_name: str, device: str, **parameters) -> nn.Module:
    if model_name == 'linear':
        return LinearClassifier(parameters['zn_size'], parameters['num_labels']).to(device)
    raise ValueError(logger.error(f'{model_name}: no such model exists !'))
