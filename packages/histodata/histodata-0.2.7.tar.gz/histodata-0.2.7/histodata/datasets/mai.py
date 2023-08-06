import os
from typing import Callable
from typing import Optional as O
from typing import Sequence
from typing import Union as U

from ..base import data_readers, df_creators, df_manipulators
from ..base.histo_dataset import HistoDataset


def mai_patches(
    root: str,
    transformation: O[U[Callable, Sequence[Callable]]] = None,
    pre_transformation: O[U[Callable, Sequence[Callable]]] = None,
    folds: O[Sequence[int]] = None,
    gt_mode: str = "GT3&GT2",
    stain_mode: str = "phh3",
    seed: O[int] = None,
):
    r"""
    The functions returns a pytorch dataset to load the MAI patches. The
    MAI patches was created in the MAI project. Pathologist annotate
    mitosis on five PHH3 WSIs. The corresponding HE slide was registered
    to he PHH3 tile. The patches have the size of 512x512 pixels and the
    label none-mitosis, G2 stadium or mitosis stands for the cell in the
    center of the image.

    Args:
        root (str): The path to the dataset.
        transformation (Callable): A callable or a list of
                       callable transformations.
        pre_transformation (Callable): A callable or a list of
                       callable transformations. "pre_transformation"
                       is called before "transformation". The transformation
                       is called with a seed and will give always the same
                       result.
        folds (list(int)): The dataset is splitted into 10 folds. The
                       last (the 9th) should be used only for testing.
                       The list contains numbers between 0 and 9.
        gt_mode (str): The pathologist take a look at the slides three times
                       (GT1, GT2, GT3). One of the following modes are allowed:
                       - "GT1": 'None-Mitosis' / 'Mitosis' from the first study
                                only at tumor regions
                       - "GT2": 'None-Mitosis' / 'Mitosis' from the second study
                                only at non-tumor regions
                       - "GT3": 'None-Mitosis' / 'G2' / 'Mitosis' from the
                                third study, only at tumor regions
                       - "GT1&GT2": Use GT1 in tumor regions and G2 in
                                none-tumor regions.
                       - "GT3&GT2": Use GT3 (with G2 as Non-Mitosis)
                                in tumor regions and G2 in non-tumor regions.
                       - "GT1=GT3": 'Non-Mitosis' / 'Mitosis'. The label mitosis
                                is only given if the first and the third study
                                marked the same region as mitosis.
                                Only tumor regions are returned.
                       - "GT1=GT3&GT2": 'Non-Mitosis' / 'Mitosis'. Same as
                                "GT1=GT3" for tumor region + "GT2" for
                                none-tumor regionen
                       - "without": no label will be returned.
        stain_mode (str): The stain to return, one of "phh3", "he", "he&phh3"
        seed (int): The seed that is used for the "pre_transformation" and the
                    "transformation". If the seed is set, the "pre_transformation"
                    will always use the same seed for a data row. If the seed is
                    set, the "transformation" will use always the same seed
                    depending on the call position. For example:
                    Call-Index,     Seed f.              Seed f.
                                pre_transformation,  transformation
                        0     ,     100           ,    124
                        1     ,     100           ,    512
                        2     ,     100           ,    810
                        3     ,     100           ,    612
                    If we create the exact same dataset the transformation seeds
                    will be the same:
                    Call-Index,     Seed f.              Seed f.
                                pre_transformation,  transformation
                        0     ,     100           ,    124
                        1     ,     100           ,    512
                        2     ,     100           ,    810
                        3     ,     100           ,    612


    Returns:
        HistoDataset: The dataset that loads the mai patches. You can use this
                      as normal pytorch dataset. If you call it you will get
                      a dictionary back.
    """
    if folds is not None:
        manipulators_to_use = [df_manipulators.ColumnFilter("fold", folds)]
    else:
        manipulators_to_use = []

    if gt_mode == "GT1&GT2":
        feature_reader = data_readers.ReadValueFromCSV(r"mitosis", encoded_values=[False, True])
    elif gt_mode == "GT3&GT2":

        def get_gt3_and_gt2(row):
            if row["area"] == "tumor":
                if row["GT3"] == "M":
                    return 1
                else:
                    return 0
            else:
                if row["mitosis"]:
                    return 1
                else:
                    return 0

        feature_reader = data_readers.ReadValueFromCSV(get_gt3_and_gt2)

    elif gt_mode == "GT1=GT3&GT2":

        def get_gt1_eq_gt3_and_gt2(row):
            if row["area"] == "tumor":
                if row["GT1_3"] == "True_M":
                    return 1
                else:
                    return 0
            else:
                if row["mitosis"]:
                    return 1
                else:
                    return 0

        feature_reader = data_readers.ReadValueFromCSV(get_gt1_eq_gt3_and_gt2)
    elif gt_mode == "GT1=GT3":
        feature_reader = data_readers.ReadValueFromCSV(r"GT1_3", encoded_values=["True_M"])
        manipulators_to_use.append(df_manipulators.ColumnFilter("area", ["tumor"]))
    elif gt_mode == "GT1":
        feature_reader = data_readers.ReadValueFromCSV(r"mitosis", encoded_values=[False, True])
        manipulators_to_use.append(df_manipulators.ColumnFilter("area", ["tumor"]))
    elif gt_mode == "GT2":
        feature_reader = data_readers.ReadValueFromCSV(r"mitosis", encoded_values=[False, True])
        manipulators_to_use.append(df_manipulators.ColumnFilter("area", ["other"]))
    elif gt_mode == "GT3":
        feature_reader = data_readers.ReadValueFromCSV(r"GT3", encoded_values=["other", "G2", "M"])
        manipulators_to_use.append(df_manipulators.ColumnFilter("GT3", ["other", "G2", "M"]))
    elif gt_mode == "without":
        feature_reader = None
    else:
        raise NotImplementedError(
            'The gt_mode must be one of the following values: ["GT1", "GT2", '
            + '"GT3", "GT1&GT2", "GT3&GT2", "GT1=GT3", "GT1=GT3&GT2"]. The'
            + ' default value is "GT3&GT2".'
        )

    if stain_mode == "phh3":
        readers_to_use = "PHH3/{id}.png"
    elif stain_mode == "he":
        readers_to_use = "HE/{id}.png"
    elif stain_mode == "he&phh3":
        readers_to_use = ["HE/{id}.png", "PHH3/{id}.png"]
    else:
        raise NotImplementedError(
            "The stain_mode must be one of the following values: "
            + '["phh3", "he", "he&phh3"]. The default value is phh3'
        )

    ds = HistoDataset(
        os.path.join(root, "data4e.csv"),
        root,
        df_manipulators=manipulators_to_use,
        data_readers=readers_to_use,
        feature_readers=feature_reader,
        seed=seed,
        pre_transfs=pre_transformation,
        da_transfs=transformation,
    )
    return ds


def mai_patches_bern(
    root: str,
    transformation: O[U[Callable, Sequence[Callable]]] = None,
    pre_transformation: O[U[Callable, Sequence[Callable]]] = None,
    stain_mode: str = "phh3",
    seed: O[int] = None,
):
    r"""
    The functions returns a pytorch dataset to load the MAI patches
    that was created from bern. There exists no labels to this dataset.

    Args:
        root (str): The path to the dataset.
        transformation (Callable): A callable or a list of
                       callable transformations.
        pre_transformation (Callable): A callable or a list of
                       callable transformations. "pre_transformation"
                       is called before "transformation". The transformation
                       is called with a seed and will give always the same
                       results.
        stain_mode (str): currently only the phh3 stain exists.
        seed (int): The seed that is used for the "pre_transformation" and the
                    "transformation". If the seed is set, the "pre_transformation"
                    will always use the same seed for a data row. If the seed is
                    set, the "transformation" will use always the same seed
                    depending on the call position. For example:
                    Call-Index,     Seed f.              Seed f.
                                pre_transformation,  transformation
                        0     ,     100           ,    124
                        1     ,     100           ,    512
                        2     ,     100           ,    810
                        3     ,     100           ,    612
                    If we create the exact same dataset the transformation seeds
                    will be the same:
                    Call-Index,     Seed f.              Seed f.
                                pre_transformation,  transformation
                        0     ,     100           ,    124
                        1     ,     100           ,    512
                        2     ,     100           ,    810
                        3     ,     100           ,    612

    Returns:
        HistoDataset: The dataset that loads the mai patches. You can use this
                      as normal pytorch dataset. If you call it you will get
                      a dictionary back.
    """
    if stain_mode == "phh3":
        readers_to_use = "PHH3/{base}.mrxs_{x}_{y}.png"
    elif stain_mode == "he_just_a_tmp_do_not_use_this":
        readers_to_use = "HE/{base}.mrxs_{x}_{y}.png"
    elif stain_mode == "he&phh3_just_a_tmp_do_not_use_this":
        readers_to_use = ["HE/{base}.mrxs_{x}_{y}.png", "PHH3/{base}.mrxs_{x}_{y}.png"]
    else:
        raise NotImplementedError(
            "The stain_mode must be one of the following values: "
            + '["phh3"]. The default value is phh3'
        )

    ds = HistoDataset(
        df_creators.CreateDFFromFolder("PHH3/{base}.mrxs_{x}_{y}.png"),
        root,
        df_manipulators=None,
        data_readers=readers_to_use,
        feature_readers=None,
        seed=seed,
        pre_transfs=pre_transformation,
        da_transfs=transformation,
    )
    return ds


def mai_he_and_phh3_fields(
    root: str,
    split: str,
    splitting_seed: O[int] = 69,
    transformation: O[U[Callable, Sequence[Callable]]] = None,
    pre_transformation: O[U[Callable, Sequence[Callable]]] = None,
    patch_size: O[int] = 224,
    overlapping_percentage: O[float] = 0.0,
    seed=None,
    stain_mode="he&phh3",
    splitting_trainings_percentage=0.8,
):
    r"""
    The functions returns a pytorch dataset to load the MAI patches. The
    MAI patches was created in the MAI project. The fields are 2048x2048
    and the stain HE and PHH3 are registered to each other. The dataset
    that is here created grids the fields into the given patch size.

    Args:
        root (str): The path to the dataset.
        split (str): which part of the dataset should be used.
                       One of {"train", "valid", "test", "all"}
        splitting_seed (int): The splitting seed that is used to create
                       the datasets.
        splitting_trainings_percentage (float): 0.0 < x < 1.0, the percentage
                       that is used for the split the train part from the
                       validation/test part. The validation and test is
                       equally splitted.
        transformation (Callable): A callable or a list of
                       callable transformations.
        pre_transformation (Callable): A callable or a list of
                       callable transformations. "pre_transformation"
                       is called before "transformation". The transformation
                       is called with a seed and will give always the same
                       result.
        patch_size (int): The size that is used for the grid. The image get
                       extracted before the transformation is called. If None,
                       the original size is returned.
        overlapping_percentage (float): 0.0 <= x < 1.0. The percentage that
                       is used for the overlapping. The value 0.5 means that
                       50 percent of one patch to the next patch are the same.
        stain_mode (str): The stain to return, one of "phh3", "he", "he&phh3"
        seed (int): The seed that is used for the "pre_transformation" and the
                    "transformation". If the seed is set, the "pre_transformation"
                    will always use the same seed for a data row. If the seed is
                    set, the "transformation" will use always the same seed
                    depending on the call position. For example:
                    Call-Index,     Seed f.              Seed f.
                                pre_transformation,  transformation
                        0     ,     100           ,    124
                        1     ,     100           ,    512
                        2     ,     100           ,    810
                        3     ,     100           ,    612
                    If we create the exact same dataset the transformation seeds
                    will be the same:
                    Call-Index,     Seed f.              Seed f.
                                pre_transformation,  transformation
                        0     ,     100           ,    124
                        1     ,     100           ,    512
                        2     ,     100           ,    810
                        3     ,     100           ,    612

    Returns:
        HistoDataset: The dataset that loads the mai patches. You can use this
                      as normal pytorch dataset. If you call it you will get
                      a dictionary back.
    """
    if patch_size is None:
        manipulators_to_use = []
    else:
        manipulators_to_use = [
            df_manipulators.EditDFImageGrid(patch_size, overlapping_percentage, (2048, 2048))
        ]
    if split == "train":
        manipulators_to_use.append(
            df_manipulators.RandomFilterByColumnValue(
                "base", splitting_trainings_percentage, mode=0, seed=splitting_seed
            )
        )
    elif split == "valid":
        manipulators_to_use.extend(
            [
                df_manipulators.RandomFilterByColumnValue(
                    "base", splitting_trainings_percentage, mode=1, seed=splitting_seed
                ),
                df_manipulators.RandomFilterByColumnValue(
                    "base", 0.5, mode=0, seed=splitting_seed + 10000
                ),
            ]
        )
    elif split == "test":
        manipulators_to_use.extend(
            [
                df_manipulators.RandomFilterByColumnValue(
                    "base", splitting_trainings_percentage, mode=1, seed=splitting_seed
                ),
                df_manipulators.RandomFilterByColumnValue(
                    "base", 0.5, mode=1, seed=splitting_seed + 10000
                ),
            ]
        )
    elif split == "all":
        pass
    else:
        raise NotImplementedError(
            'The parameter "split" needs to be one of ["train", "valid", "test", "all"].'
        )

    if stain_mode == "phh3":
        readers_to_use = data_readers.ReadFromImageFile(
            "{base}/{base}.phh3.png", return_image_size=patch_size
        )
    elif stain_mode == "he":
        readers_to_use = data_readers.ReadFromImageFile(
            "{base}/{base}.he.png", return_image_size=patch_size
        )
    elif stain_mode == "he&phh3":
        readers_to_use = [
            data_readers.ReadFromImageFile("{base}/{base}.he.png", return_image_size=patch_size),
            data_readers.ReadFromImageFile("{base}/{base}.phh3.png", return_image_size=patch_size),
        ]
    else:
        raise NotImplementedError(
            "The stain_mode must be one of the following values: "
            + '["phh3", "he", "he&phh3"]. The default value is phh3'
        )

    ds = HistoDataset(
        df_creators.CreateDFFromFolder("{base}/{base}.he.png"),
        root,
        data_readers=readers_to_use,
        df_manipulators=manipulators_to_use,
        seed=seed,
        pre_transfs=pre_transformation,
        da_transfs=transformation,
    )
    return ds


def mai_slides(
    root,  # '/data/ldap/histopathologic/original_read_only/MAI/slides
    transformation=None,
    pre_transformation=None,
    patch_size=224,
    overlapping_percentage=0.0,  # TODO
    seed=None,
    stain_mode="all",  # one of ["he", "phh3", "all"]
    scanner_mode="all",  # one of ["xr", "p1000", "p150", "all"]
    location_mode="all",  # one of ["bern", "charite", "all"]
    mpp=0.5,
):
    if stain_mode == "all":
        stain = "{stain}"

    elif stain_mode in ("he", "phh3"):
        stain = stain_mode
    else:
        raise NotImplementedError()

    if location_mode == "all":
        location = "{location}"
    elif location_mode in ("bern", "charite"):
        location = stain_mode
    else:
        raise NotImplementedError()

    if scanner_mode == "all":
        scanner = "{scanner}"
    elif scanner_mode in ("xr", "p1000", "p150"):
        scanner = scanner_mode
    else:
        raise NotImplementedError()

    ds = HistoDataset(
        df_creators.CreateDFFromFolder(
            location + "/" + stain + "/" + scanner + "/{name}\\.(ndpi|mrxs)"
        ),
        root,
        df_manipulators=df_manipulators.EditDFWSIGrid(
            patch_size, perc_overlapping=overlapping_percentage
        ),
        data_readers=data_readers.ReadFromWSI(patch_size, "__path__", mpp=mpp),
        seed=seed,
        pre_transfs=pre_transformation,
        da_transfs=transformation,
    )
    return ds
