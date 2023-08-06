import pickle

import torch
from torch.nn.utils.rnn import pad_sequence
from torch.utils.data import Dataset
from transformers import CamembertTokenizerFast


class CamemBertNerDataset(Dataset):
    def __init__(self, dataset: list, tokenizer: CamembertTokenizerFast):
        self.tokenizer = tokenizer
        self.dataset = dataset
        self.pad_id = tokenizer.pad_token_id

    def __getitem__(self, index) -> dict:
        example = pickle.load(open(self.dataset[index], "rb"))
        return {
            "tokens": example["sub_tokens_ids"],
            "target": example["labels_ids"],
        }

    def __len__(self) -> int:
        return len(self.dataset)

    def masked_lm_collate(self, batch: list):
        tokens = self.pad_batch(batch, "tokens", self.pad_id)
        target = self.pad_batch(batch, "target", -100)
        attention_mask = (tokens != self.pad_id).int()

        return {"tokens": tokens, "attention_mask": attention_mask, "target": target}

    @staticmethod
    def pad_batch(batch, element_name, pad_id):
        return pad_sequence(
            [torch.LongTensor(example[element_name]) for example in batch],
            batch_first=True,
            padding_value=pad_id,
        )
