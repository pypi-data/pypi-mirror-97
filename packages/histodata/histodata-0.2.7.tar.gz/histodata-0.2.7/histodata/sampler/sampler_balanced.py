from typing import Sequence

import numpy as np
import torch
import torch.utils


class SamplerBalanced(torch.utils.data.Sampler[int]):
    r"""Samples elements class balanced. If shuffle is False, this sampler works like
    undersampling. But if shuffle True, the elements get shuffled each epoch.

    Arguments:
        data_labels: the labels of each element of the dataset.
        batch_size: the number of ids that this sampler should return in one call.
        shuffle: If true, the elements get shuffled each epoch.
    """

    def __init__(
        self, data_labels: Sequence[int], batch_size: int = 64, shuffle: bool = True
    ) -> None:
        super().__init__(data_source=None)

        self.data_labels = data_labels
        self.batch_size = batch_size
        self.shuffle = shuffle

    @property
    def num_samples(self) -> int:
        return len(self.data_labels)

    def __iter__(self):
        number_of_classes = np.max(self.data_labels) + 1
        indices = []
        num_of_samples_each_class = []
        for class_label in range(number_of_classes):
            indices_of_class = np.argwhere(self.data_labels == class_label)[:, 0]
            if self.shuffle:
                np.random.shuffle(indices_of_class)
            indices.append(indices_of_class)
            num_of_samples_each_class.append(len(indices_of_class))

        num_of_samples = np.min(num_of_samples_each_class)

        bz_each_label = self.batch_size // number_of_classes

        num_of_batches = num_of_samples // bz_each_label

        for i in range(num_of_batches):
            indices_to_return = []
            for class_label in range(number_of_classes):
                indices_to_return.extend(
                    indices[class_label][i * bz_each_label : (i + 1) * bz_each_label]
                )
            yield indices_to_return

    def __len__(self):
        return len(self.data_labels)  # // self.batch_size
