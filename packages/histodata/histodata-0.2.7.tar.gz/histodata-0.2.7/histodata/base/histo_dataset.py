import random
from typing import Callable
from typing import Optional as O
from typing import Sequence
from typing import Union as U

import numpy as np
import pandas as pd
import torch
import torch.utils

from ..helper import helper
from . import data_readers as readers
from . import df_creators
from .data_readers import Reader
from .df_creators import DataFrameCreator
from .df_manipulators import DataFrameManipulator
from .transformer_handler import TransformerHandler


class HistoDataset(torch.utils.data.Dataset):
    def __init__(
        self,
        df_creator: U[str, DataFrameCreator],
        path_to_dataset: str,
        df_manipulators: O[U[Sequence[DataFrameManipulator], DataFrameManipulator]] = None,
        data_readers: O[U[str, Reader, Sequence[U[str, Reader]]]] = None,
        feature_readers: O[U[str, Reader, Sequence[U[str, Reader]]]] = None,
        pre_transfs: O[U[TransformerHandler, Callable, Sequence[Callable]]] = None,
        da_transfs: O[U[TransformerHandler, Callable, Sequence[Callable]]] = None,
        seed: int = None,
        return_index: bool = False,
        return_pytorch_tensor: bool = True,
    ):
        super().__init__()

        # save variables
        self.path_to_dataset = path_to_dataset
        self.return_index = return_index
        self.seed = seed
        self.seed_increment = 0
        self.return_pytorch_tensor = return_pytorch_tensor

        # create a DataFrameCreator if str was given
        if isinstance(df_creator, str):
            df_creator = df_creators.CreateDFFromCSV(df_creator)

        # convert or create list of data_readers
        self.data_readers = helper.create_dict_from_variable(data_readers, "data")
        for name in self.data_readers:
            if isinstance(self.data_readers[name], str):
                self.data_readers[name] = readers.ReadFromImageFile(self.data_readers[name])

        # convert or create list of feature_readers
        self.feature_readers = helper.create_dict_from_variable(feature_readers, "feature")
        for name in self.feature_readers:
            if isinstance(self.feature_readers[name], str):
                self.feature_readers[name] = readers.ReadValueFromCSV(self.feature_readers[name])

        # convert or create list of pre_transformation-handler
        if isinstance(pre_transfs, TransformerHandler):
            self.pre_transfs = pre_transfs
        else:
            if self.seed is None:
                self.pre_transfs = TransformerHandler(
                    pre_transfs, seed=random.randint(0, 99999999999)
                )
            else:
                self.pre_transfs = TransformerHandler(pre_transfs, seed=self.seed * int(1e3))

        # convert or create list of da_transformation-handler
        if isinstance(da_transfs, TransformerHandler):
            self.da_transfs = da_transfs
        else:
            self.da_transfs = TransformerHandler(da_transfs)

        # read csv file
        self.df = df_creator(self.path_to_dataset)

        # manipulate the data frame
        if df_manipulators is not None:
            main_data_reader = self.data_readers[list(self.data_readers)[0]]
            if isinstance(df_manipulators, list):
                for df_mani in df_manipulators:
                    self.df = df_mani(self.df, self.path_to_dataset, main_data_reader)
            else:
                self.df = df_manipulators(self.df, self.path_to_dataset, main_data_reader)

        # make sure that the indizes starts by 0
        self.df.reset_index(inplace=True, drop=True)

        # create hash for each row
        self.df["__hash_of_row__"] = self.df.apply(lambda row: int(hash(str(row.values)) % 1e17), 1)

        # for preloading the images / labels
        self.preloaded_data = None
        self.preloaded_features = None

    def preload(self, batch_size=128):
        self.preloaded_data = {}
        self.preloaded_features = {}
        for i in range(0, len(self.df), batch_size):
            data = self.__load_data__(self.df.iloc[i : i + batch_size].index)
            features = self.__load_features__(self.df.iloc[i : i + batch_size].index)

            for k in data:
                if k in self.preloaded_data:
                    self.preloaded_data[k].extend(data[k])
                else:
                    self.preloaded_data[k] = data[k]

            for k in features:
                if k in self.preloaded_features:
                    self.preloaded_features[k].extend(features[k])
                else:
                    self.preloaded_features[k] = features[k]

    def __load_data__(self, idx):
        # get asked row
        row = self.df.iloc[idx]

        # load data
        data = {}
        for key, img_loader in self.data_readers.items():
            loaded = img_loader(row, self.path_to_dataset)
            if isinstance(loaded, dict):
                for k in loaded:
                    data[key + "_" + k] = loaded[k]
            else:
                data[key] = loaded

        # pre transform
        data = self.pre_transfs(data, self.__get_hash__(idx))

        return data

    def __load_features__(self, idx):
        # get asked row
        row = self.df.iloc[idx]

        features = {
            key: feature_loader(row, self.path_to_dataset)
            for key, feature_loader in self.feature_readers.items()
        }

        return features

    def __len__(self):
        return len(self.df)

    def __get_hash__(self, idx):
        # get hashes
        row = self.df.iloc[idx]
        hashes = row["__hash_of_row__"]
        if isinstance(hashes, pd.Series):
            hashes = hashes.values.tolist()
        return hashes

    def __convert_to_tensor__(self, data, idx):
        for key in data:
            if isinstance(idx, list):
                if isinstance(data[key], list):
                    if not torch.is_tensor(data[key][0]):
                        for i, d in enumerate(data[key]):
                            if isinstance(d, np.ndarray):
                                data[key][i] = torch.as_tensor(d.copy())
                            else:
                                data[key][i] = torch.as_tensor(d)
                    data[key] = torch.stack(data[key])
                elif not torch.is_tensor(data[key]):
                    data[key] = torch.as_tensor(data[key])
            elif not torch.is_tensor(data[key]):
                if isinstance(data[key], np.ndarray):
                    data[key] = torch.as_tensor(data[key].copy())
                else:
                    data[key] = torch.as_tensor(data[key])
        return data

    def get_features(self, idx):
        if isinstance(idx, np.ndarray):
            idx = list(idx)

        if self.preloaded_data is None:
            features = self.__load_features__(idx)
        else:
            features = {}
            for k in self.preloaded_features:
                if isinstance(idx, list):
                    features[k] = [self.preloaded_features[k][_idx] for _idx in idx]
                else:
                    features[k] = self.preloaded_features[k][idx]
        if self.return_pytorch_tensor:
            features = self.__convert_to_tensor__(features, idx)

        return features

    def get_feature_for_all_rows(self):
        if self.preloaded_data is not None:
            return self.preloaded_features
        else:
            return self.get_features(np.arange(len(self)))

    def __getitem__(self, idx):
        if isinstance(idx, np.ndarray):
            idx = list(idx)

        if self.seed is not None:
            # save random state to reactivate this state after the call
            saved_seed_state = helper.get_random_seed()
            # set seets
            worker_info = torch.utils.data.get_worker_info()
            if worker_info is None:
                worker_id = 0
                num_workers = 1
            else:
                worker_id = worker_info.id
                num_workers = worker_info.num_workers
            seed_to_set = (1 + self.seed_increment + worker_id) * int(1e7) + self.seed

            helper.set_random_seed_with_int(seed_to_set)
            # increase seed increment to use a new random seed at next call
            self.seed_increment += num_workers

        if self.preloaded_data is None:
            data = self.__load_data__(idx)
            features = self.__load_features__(idx)
        else:
            data = {}
            for k in self.preloaded_data:
                if isinstance(idx, list):
                    data[k] = [self.preloaded_data[k][_idx] for _idx in idx]
                else:
                    data[k] = self.preloaded_data[k][idx]
            features = {}
            for k in self.preloaded_features:
                if isinstance(idx, list):
                    features[k] = [self.preloaded_features[k][_idx] for _idx in idx]
                else:
                    features[k] = self.preloaded_features[k][idx]

        # da transforms
        data = self.da_transfs(data, self.__get_hash__(idx))

        if self.seed is not None:
            # reactivate random state
            helper.set_random_seed(*saved_seed_state)

        if self.return_pytorch_tensor:
            data = self.__convert_to_tensor__(data, idx)
            features = self.__convert_to_tensor__(features, idx)

        dic = {}
        dic.update(data)
        dic.update(features)
        if self.return_index:
            dic["idx"] = idx
        return dic
