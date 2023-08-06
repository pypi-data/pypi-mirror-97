import os

from ..base import data_readers, df_creators, df_manipulators
from ..base.histo_dataset import HistoDataset


def bach_patches(
    root,  # '/data/ldap/histopathologic/original_read_only/BACH/ICIAR2018_BACH_Challenge'
    transformation=None,
    pre_transformation=None,
    split="all",
    splitting_seed=69,
    splitting_trainings_percentage=0.8,
    seed=None,
    patch_size=224,
    overlapping_percentage=0.0,
):
    manipulators_to_use = [
        df_manipulators.EditDFImageGrid(patch_size, overlapping_percentage, (1536, 2048))
    ]
    if split == "train":
        manipulators_to_use.append(
            df_manipulators.RandomFilterByColumnValue(
                "file_name", splitting_trainings_percentage, mode=0, seed=splitting_seed
            )
        )
    elif split == "valid":
        manipulators_to_use.extend(
            [
                df_manipulators.RandomFilterByColumnValue(
                    "file_name", splitting_trainings_percentage, mode=1, seed=splitting_seed
                ),
                df_manipulators.RandomFilterByColumnValue(
                    "file_name", 0.5, mode=0, seed=splitting_seed + 10000
                ),
            ]
        )
    elif split == "test":
        manipulators_to_use.extend(
            [
                df_manipulators.RandomFilterByColumnValue(
                    "file_name", splitting_trainings_percentage, mode=1, seed=splitting_seed
                ),
                df_manipulators.RandomFilterByColumnValue(
                    "file_name", 0.5, mode=1, seed=splitting_seed + 10000
                ),
            ]
        )
    elif split == "all":
        pass
    else:
        raise NotImplementedError(
            'The parameter "split" needs to be one of ["train", "valid", "test", "all"].'
        )

    path_to_csv = os.path.join(root, "Photos/microscopy_ground_truth.csv")
    ds = HistoDataset(
        df_creators.CreateDFFromCSV(path_to_csv, header=None, names=["file_name", "label"]),
        root,
        df_manipulators=manipulators_to_use,
        data_readers="Photos/{label}/{file_name}",
        feature_readers=data_readers.ReadValueFromCSV(
            r"{label}", encoded_values=["Benign", "InSitu", "Invasive", "Normal"]
        ),
        seed=seed,
        pre_transfs=pre_transformation,
        da_transfs=transformation,
    )
    return ds
