import random
from enum import IntEnum

import numpy as np
import torch


class DataLoaderMode(IntEnum):
    TRAINING = 1
    VALIDATION = 2
    TRAINING_AND_VALIDATION = 3
    TEST = 4
    ALL = 7


def collate_fn(
    batch,
):  # Here we would need two collate function for train and validation!
    r"""
    This collate_fn function can be used with the "SamplerSimple" and "SamplerBalanced".
    The batch size should be set in the Sampler and not in the DataLoader.
    """
    data = batch[0][0]
    target = torch.as_tensor(batch[0][1], dtype=torch.int64)

    return data, target


# EIGENE FUNKTIOn, bekommt ein DATASET und splitted diese in zwei oder drei neue Datasets
# mode: DataLoaderMode,
# cross_validation_fold: O[U[Sequence[int], int]] = None,


def create_circular_mask(h, w, center=None, radius=None):

    if center is None:  # use the middle of the image
        center = (int(w / 2), int(h / 2))
    if radius is None:  # use the smallest distance between the center and image walls
        radius = min(center[1], center[0], w - center[1], h - center[0])

    y, x = np.ogrid[:h, :w]
    dist_from_center = np.sqrt((y - center[1]) ** 2 + (x - center[0]) ** 2)

    mask = dist_from_center <= radius
    return mask


def create_list_from_variable(variable):
    if variable is None:
        return []
    elif isinstance(variable, list):
        return variable
    else:
        return [variable]


def create_dict_from_variable(variable, default_name):
    if variable is None:
        return {}
    elif isinstance(variable, list):
        dic = {}
        for idx, element in enumerate(variable):
            dic[str(default_name) + "_" + str(idx)] = element
        return dic
    elif isinstance(variable, dict):
        return variable
    else:
        return {default_name: variable}


def get_random_seed():
    module_random = random.getstate()
    module_numpy = np.random.get_state()
    module_torch = torch.get_rng_state()
    return module_random, module_numpy, module_torch


def set_random_seed(module_random, module_numpy, module_torch):
    random.setstate(module_random)
    np.random.set_state(module_numpy)
    torch.set_rng_state(module_torch)


def set_random_seed_with_int(integer):
    random.seed(integer)
    np.random.seed(random.randint(0, 99999999))
    torch.random.manual_seed(random.randint(0, 99999999))


def read_from_row(row, expression):
    return expression.format(**row)


def labels_to_weights(labels):
    labels = np.array(labels)
    label_prob = np.zeros_like(labels, dtype=np.float)
    for l in np.unique(labels):
        prob = sum(labels == l) / float(len(labels))
        label_prob[labels == l] = 1 - prob
    return label_prob
