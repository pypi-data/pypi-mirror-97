from pathlib import Path
import h5py
from .parsers import make_structured_array
from .preprocess import accumulate_frames, slice_by_time, create_raster_from_xytp
import numpy as np


class HDF5FolderDataset:
    """
    Base class to load .h5 files of a dataset from a folder and its sub-folders.

    Args:
        source_folder (str, Path): Path of the source folder
        transform (callable, None): Method to transform the data
        target_transform (callable, None): Method to transform targets
    """
    def __init__(
            self,
        source_folder,
        transform=None,
        target_transform=None,
    ):
        types = ("**/*.h5")
        self.file_list = sorted(Path(source_folder).glob(types))
        self.transform = transform
        self.target_transform = target_transform

        if len(self.file_list) == 0:
            raise FileNotFoundError("No files found in" + str(source_folder))

    def __len__(self):
        return len(self.file_list)

    @staticmethod
    def _pick_data_from_file(file):
        raise NotImplementedError()

    def __getitem__(self, i):
        # opening file
        file = self.file_list[i]
        with h5py.File(file, "r") as F:
            data = self._pick_data_from_file(F)
            label = F["label"][()]

        if self.transform is not None:
            data = self.transform(data)
        if self.target_transform is not None:
            label = self.target_transform(label)

        return data, label


class FramesDataset(HDF5FolderDataset):
    """
    Dataset iterator that loads .h5 files of a dataset from a folder and its sub-folders.
    The iterator returns two values per sample: frame, label

    Args:
        source_folder (str, Path): Path of the source folder
        transform (callable, None): Method to transform the data
        target_transform (callable, None): Method to transform targets
    """
    def __init__(
            self,
        source_folder,
        transform=None,
        target_transform=None,
    ):
        super().__init__(
            source_folder=source_folder,
            transform=transform,
            target_transform=target_transform
        )

    @staticmethod
    def _pick_data_from_file(file):
        return file["frame"][()].astype(np.float32)


class SpikeTrainDataset(HDF5FolderDataset):
    """
    Dataset iterator that loads .h5 files of a dataset from a folder and its sub-folders.
    The iterator returns two values per sample:
    - if dt is None: xytp, label
    - if dt is int: np.ndarray, label

    Args:
        source_folder (str, Path): Path of the source folder
        transform (callable, None): Method to transform the data
        target_transform (callable, None): Method to transform targets
        dt (int, None): Time window to bin the spikes into if the data produced is expected to be rasterized.
    """
    def __init__(
        self,
        source_folder,
        transform=None,
        target_transform=None,
        dt=None,
        bins=None,
    ):
        super().__init__(
            source_folder=source_folder,
            transform=transform,
            target_transform=target_transform
        )

        self.dt = dt

    def _pick_data_from_file(self, file):
        xytp = make_structured_array(
            file["spikes"]["x"][()],
            file["spikes"]["y"][()],
            file["spikes"]["t"][()],
            file["spikes"]["p"][()]
        )
        bins_yx = (file["bins"]["y"][()], file["bins"]["x"][()])

        if self.dt is None:
            return xytp
        else:
            return create_raster_from_xytp(xytp, self.dt, *bins_yx)
