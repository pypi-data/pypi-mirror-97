import numpy as np
import torch
import torch.utils


class SamplerSimple(torch.utils.data.Sampler[int]):
    r"""Samples elements sequentielly.

    Arguments:
        num_of_samples: The number of data samples that the dataset have.
        batch_size: the number of ids that this sampler should return in one call.
        shuffle: If true, the elements get shuffled each epoch.
    """

    def __init__(self, num_of_samples: int, batch_size: int = 64, shuffle: bool = False) -> None:
        super().__init__(data_source=None)

        self.num_of_samples = num_of_samples
        self.batch_size = batch_size
        self.shuffle = shuffle

    @property
    def num_samples(self) -> int:
        return self.num_of_samples

    def __iter__(self):
        indices = np.arange(self.num_of_samples)

        if self.shuffle:
            np.random.shuffle(indices)

        num_of_batches = len(indices) // self.batch_size

        for i in range(num_of_batches):
            yield indices[i * self.batch_size : (i + 1) * self.batch_size]

        if len(indices) > num_of_batches * self.batch_size:
            yield indices[num_of_batches * self.batch_size :]

    def __len__(self):
        return self.num_of_samples  # // self.batch_size
