import math
import random

import matplotlib.pyplot as plt
import numpy as np
import openslide
import pandas as pd
from scipy.ndimage.measurements import center_of_mass
from skimage import morphology
from skimage.color import rgb2hed
from skimage.filters import threshold_otsu
from skimage.segmentation import slic


class DataFrameManipulator:
    def __init__(self):
        pass

    def __call__(self, df, path_to_image, reader):
        pass


class EditDFImageGrid(DataFrameManipulator):
    def __init__(self, return_image_size, perc_overlapping=0.0, input_im_size=None):
        super().__init__()
        self.return_image_size = return_image_size
        self.perc_overlapping = perc_overlapping
        self.input_im_size = input_im_size

    def get_points(self, im_size1d):
        im_size_center = im_size1d - self.return_image_size
        shift = self.return_image_size * (1 - self.perc_overlapping)
        locations = np.arange(0, im_size_center + 0.0001, shift)

        return np.array(locations + (im_size1d - locations[-1]) / 2, dtype=int)

    def __call__(self, df, path_to_image, reader):
        if self.input_im_size is not None:
            input_im_size = self.input_im_size

        rows = {name: [] for name in list(df)}
        rows["__x__"] = []
        rows["__y__"] = []
        for _, row in df.iterrows():
            if self.input_im_size is None:
                input_im_size = reader.get_image_size(row, path_to_image)
            xs = self.get_points(input_im_size[0])
            ys = self.get_points(input_im_size[1])

            for x in xs:
                for y in ys:
                    row = dict(row)
                    row["__x__"] = x
                    row["__y__"] = y

                    for k in row:
                        rows[k].append(row[k])

        return pd.DataFrame(rows)


def get_mask(rgb):
    rgb = np.array(rgb, dtype=float) / 255.0

    ihc_hed = rgb2hed(rgb)

    gray = ihc_hed[..., 0] + ihc_hed[..., 1]  # - ihc_hed[..., 2]

    counts, positions = np.histogram(gray.flatten(), bins=50, range=(0.001, 0.04))
    argmax = np.argmax(counts)

    threshold1 = None
    threshold2 = None

    for pos in range(argmax, 48):
        if threshold1 is None:
            if counts[pos + 1] > counts[pos] and counts[pos + 2] > counts[pos + 1]:
                threshold1 = positions[pos]
        if threshold2 is None:
            if counts[pos + 1] > counts[pos]:
                threshold2 = positions[pos]
    if threshold1 is not None:
        threshold = threshold1
    elif threshold2 is not None:
        threshold = threshold2
    else:
        threshold = 0.04

    # use otsu as second threshold
    values_for_otsu = gray.flatten()
    values_for_otsu = values_for_otsu[values_for_otsu > 0.001]
    values_for_otsu = values_for_otsu[values_for_otsu < 0.04]
    threshold_from_otsu = threshold_otsu(values_for_otsu)

    # use the smaller threshold
    mask = gray > min([threshold, threshold_from_otsu])

    mask = morphology.binary_opening(mask, morphology.disk(1))
    mask = morphology.binary_closing(mask, morphology.disk(1))
    mask = morphology.binary_opening(mask, morphology.disk(3))
    mask = morphology.binary_closing(mask, morphology.disk(9))

    return mask


class EditDFWSIGrid(DataFrameManipulator):
    def __init__(
        self,
        return_image_size,
        perc_overlapping=0.0,
        plt_coordinates=False,
        fn_thumbnail_to_mask=get_mask,
    ):
        super().__init__()
        self.return_image_size = return_image_size
        self.perc_overlapping = perc_overlapping
        self.plt_coordinates = plt_coordinates
        self.fn_thumbnail_to_mask = fn_thumbnail_to_mask

    def __get_coordinates__(self, thumbnail, thumbnail_mpp, return_mpp, min_mpp):
        return_mpp = float(return_mpp)
        thumbnail_mpp = float(thumbnail_mpp)
        # see: https://colab.research.google.com/github/TIA-Lab
        # /tiatoolbox/blob/master/examples/example_wsiread.ipynb#scrollTo=MZ_yqoGJ_-6i
        wsi_thumb_mask = self.fn_thumbnail_to_mask(thumbnail)

        return_image_stride = self.return_image_size * (1 - self.perc_overlapping)

        lores_patch_size = int(return_image_stride / (thumbnail_mpp / return_mpp))
        nr_expected_rois = math.ceil(np.sum(wsi_thumb_mask) / (lores_patch_size ** 2))

        print(f"Created ~{nr_expected_rois} patches.")

        wsi_rois_mask = slic(
            thumbnail, mask=wsi_thumb_mask, n_segments=nr_expected_rois, compactness=1000, sigma=1
        )

        lores_rois_center = center_of_mass(
            wsi_rois_mask, labels=wsi_rois_mask, index=np.unique(wsi_rois_mask)[1:]
        )
        lores_rois_center = np.array(lores_rois_center)  # coordinates is Y, X
        lores_rois_center = lores_rois_center.astype(np.int32)
        selected_indices = wsi_thumb_mask[lores_rois_center[:, 0], lores_rois_center[:, 1]]
        lores_rois_center = lores_rois_center[selected_indices]

        distance_to_boarder = []
        for center_x, center_y in zip(lores_rois_center[:, 1], lores_rois_center[:, 0]):
            y, x = np.ogrid[: wsi_thumb_mask.shape[0], : wsi_thumb_mask.shape[1]]
            dist_from_center = np.sqrt((y - center_y) ** 2 + (x - center_x) ** 2)
            dist = np.min(dist_from_center[~wsi_thumb_mask])
            distance_to_boarder.append(dist)
        distance_to_boarder = np.array(distance_to_boarder)

        if self.plt_coordinates:
            # show the patches region and their centres of mass
            plt.figure(figsize=(20, 6))
            plt.subplot(1, 4, 1)
            # plt.subfigure(subf)
            plt.imshow(thumbnail)
            plt.subplot(1, 4, 2)
            plt.imshow(thumbnail)
            plt.scatter(lores_rois_center[:, 1], lores_rois_center[:, 0], s=5)
            plt.scatter(lores_rois_center[0:1, 1], lores_rois_center[0:1, 0], s=18, c="g")
            plt.scatter(lores_rois_center[1:2, 1], lores_rois_center[1:2, 0], s=18, c="y")
            plt.axis("off")
            plt.subplot(1, 4, 3)
            plt.scatter(
                lores_rois_center[:, 1], -lores_rois_center[:, 0], c=distance_to_boarder, s=5
            )
            plt.axis("off")
            plt.subplot(1, 4, 4)
            plt.imshow(wsi_thumb_mask)
            plt.show()

        return lores_rois_center * (thumbnail_mpp / min_mpp), distance_to_boarder * (
            thumbnail_mpp / min_mpp
        )

    def __call__(self, df, path_to_image, reader):

        rows = {name: [] for name in list(df)}
        rows["__x__"] = []
        rows["__y__"] = []
        rows["__dist__"] = []
        for _, row in df.iterrows():
            try:
                thumbnail, min_mpp = reader.read_thumbnail(
                    row, path_to_image, 20, return_min_mpp=True
                )
            except openslide.OpenSlideUnsupportedFormatError:
                print("Warning: The file is damaged or has missing files.")
                continue
            coordinates, distance_to_boarders = self.__get_coordinates__(
                thumbnail, 20, reader.mpp, min_mpp[0]
            )

            for x, y, dist in zip(coordinates[:, 1], coordinates[:, 0], distance_to_boarders):
                row = dict(row)
                row["__x__"] = int(x)
                row["__y__"] = int(y)
                row["__dist__"] = dist

                for k in row:
                    rows[k].append(row[k])

        return pd.DataFrame(rows)


class DataFrameFilter:
    def __init__(self, mode):
        self.mode = mode

    def __call__(self, df, indices):
        if self.mode == 0:
            return df.loc[indices]
        elif self.mode == 1:
            return df.loc[~df.index.isin(indices)]
        else:
            return df.loc[indices], df.loc[~df.index.isin(indices)]


class RandomFilter(DataFrameFilter, DataFrameManipulator):
    def __init__(self, percentage_to_filter, mode=0, seed=None):
        DataFrameFilter.__init__(self, mode)
        DataFrameManipulator.__init__(self)
        self.percentage_to_filter = percentage_to_filter
        self.seed = seed

    def __call__(self, df, path_to_image, reader):
        r = random.Random(self.seed)
        indices = r.sample(list(df.index), int(len(df) * self.percentage_to_filter))
        return DataFrameFilter.__call__(self, df, indices)


class RandomFilterByColumnValue(DataFrameFilter, DataFrameManipulator):
    def __init__(self, column, percentage_to_filter, mode=0, seed=None):
        DataFrameFilter.__init__(self, mode)
        DataFrameManipulator.__init__(self)
        self.column = column
        self.percentage_to_filter = percentage_to_filter
        self.seed = seed

    def __call__(self, df, path_to_image, reader):
        uv = list(df[self.column].unique())
        r = random.Random(self.seed)
        choosen = r.sample(uv, int(len(uv) * self.percentage_to_filter))
        indices = list(df[df[self.column].isin(choosen)].index)
        return DataFrameFilter.__call__(self, df, indices)


class LambdaFilter(DataFrameFilter, DataFrameManipulator):
    def __init__(self, lambda_function, mode=0):
        DataFrameFilter.__init__(self, mode)
        DataFrameManipulator.__init__(self)
        self.lambda_function = lambda_function

    def __call__(self, df, path_to_image, reader):
        return DataFrameFilter.__call__(self, df, df[df.apply(self.lambda_function, 1)].index)


class ColumnFilter(DataFrameFilter, DataFrameManipulator):
    def __init__(self, name_of_column, allowed_values, mode=0):
        DataFrameFilter.__init__(self, mode)
        DataFrameManipulator.__init__(self)
        self.name_of_column = name_of_column
        self.allowed_values = allowed_values

    def __call__(self, df, path_to_image, reader):
        if isinstance(self.allowed_values, list):
            return DataFrameFilter.__call__(
                self, df, df[df[self.name_of_column].isin(self.allowed_values)].index
            )
        else:
            return DataFrameFilter.__call__(
                self, df, df[df[self.name_of_column] == self.allowed_values].index
            )
