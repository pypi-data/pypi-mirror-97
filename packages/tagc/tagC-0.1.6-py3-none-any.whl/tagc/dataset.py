import random

import torch
from sklearn.preprocessing import MultiLabelBinarizer
from torch.utils.data import Dataset
from transformers import AutoTokenizer

from .data_utils import compose, grouping_idx
from .domain import Params

random.seed(42)


class CustomDataset(Dataset):
    def __init__(self, texts, tokenizer: AutoTokenizer, max_len: int, tags=None):
        self.tokenizer = tokenizer
        self.texts = texts
        self.tags = tags
        self.max_len = max_len

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, index):
        text = self.texts[index]

        inputs = self.tokenizer.encode_plus(
            text,
            None,
            add_special_tokens=True,
            truncation=True,
            max_length=self.max_len,
            padding="max_length",
            return_token_type_ids=True,
        )
        ids = inputs["input_ids"]
        mask = inputs["attention_mask"]
        token_type_ids = inputs["token_type_ids"]

        if self.tags is None:
            return {
                "input_ids": torch.tensor(ids, dtype=torch.long),
                "attention_mask": torch.tensor(mask, dtype=torch.long),
                "token_type_ids": torch.tensor(token_type_ids, dtype=torch.long),
            }

        return {
            "input_ids": torch.tensor(ids, dtype=torch.long),
            "attention_mask": torch.tensor(mask, dtype=torch.long),
            "token_type_ids": torch.tensor(token_type_ids, dtype=torch.long),
            "labels": torch.tensor(self.tags[index], dtype=torch.float),
        }


class DatasetFactory:
    def __init__(self, params: Params):
        self.params = params
        raw_data = params.raw_data
        self.x_test_dict = raw_data.x_test_dict
        self.x_train_dict = raw_data.x_train_dict
        self.y_train_tags = raw_data.y_train_tags
        self.y_test_tags = raw_data.y_test_tags
        if params.mlb is not None:
            self.mlb = params.mlb
            self.num_labels = len(self.mlb.classes_)
        else:
            self.init_mlb()
        self.init_tokenizer(params.identifier)

    def init_mlb(self):
        y = self.y_train_tags + self.y_test_tags
        mlb = MultiLabelBinarizer().fit(y)
        self.mlb = mlb
        self.num_labels = len(self.mlb.classes_)

    def init_tokenizer(self, identifier: str):
        self.tokenizer = AutoTokenizer.from_pretrained(identifier)

    def supply_training_dataset(self):
        x_train, y_train_raw = self._upsampling(
            self.x_train_dict, self.y_train_tags, target=self.params.upsampling
        )
        y_train = self.mlb.transform(y_train_raw)
        x_test = list(map(compose, self.x_test_dict))
        y_test = self.mlb.transform(self.y_test_tags)
        train_dataset = CustomDataset(
            x_train, self.tokenizer, self.params.max_len, y_train
        )
        testing_set = CustomDataset(x_test, self.tokenizer, self.params.max_len, y_test)
        return train_dataset, testing_set

    def _upsampling(self, x, y, target=100):

        group_by_idx = grouping_idx(y)
        new_x = []
        new_y = []
        if target < 0:
            shuffle = False
            size = abs(target)
        else:
            shuffle = True
            size = target
        for group_idx in group_by_idx.values():
            upsample_idx = random.choices(group_idx, k=size)
            new_x.extend(
                map(lambda idx: self._compose(x[idx], shuffle=shuffle), upsample_idx)
            )
            new_y.extend(map(lambda idx: y[idx], upsample_idx))
        return new_x, new_y

    def _compose(self, case, shuffle=True):
        return compose(case, keep_key=self.params.keep_key, shuffle=shuffle)
