import numpy as np
from typing import Tuple, List


def crop_events(xytp: np.ndarray, input_shape: Tuple, crop_size: Tuple):
    """
    Crop events

    Args:
        xytp (np.ndarray):  Structured array of events
        input_shape (Tuple): A tuple (height, width)
        crop_size (Tuple(Tuple)): A tuple of the borders to crop ((left, right), (top, bottom))

    Returns:
        cropped_xytp (np.ndarray): Structured array of events.
        The pixel addresses are shifted to origin after cropping
    """
    (left, right), (top, bottom) = crop_size
    x_lo, y_lo = 0, 0
    y_hi, x_hi, = input_shape
    x_hi -= 1
    y_hi -= 1

    x, y = xytp["x"], xytp["y"]

    keepidx = (
            (x >= x_lo + left)
            & (x <= x_hi - right)
            & (y >= y_lo + top)
            & (y <= y_hi - bottom)
    )

    xytp_cropped = xytp[keepidx]
    xytp_cropped["x"] -= left
    xytp_cropped["y"] -= top

    new_shape = (input_shape[0] - top - bottom), (input_shape[1] - left - right)

    return xytp_cropped, new_shape


def crop_frame(frame: np.ndarray, crop_size: Tuple):
    """
    Crop events

    Args:
        frame(np.ndarray): numpy array of a frame of dimensions (channels, height, width)
        crop_size (Tuple(Tuple)): A tuple of the borders to crop ((left, right), (top, bottom))

    Returns:
        cropped_frame (np.ndarray): numpy array of a frame of dimensions (channels, height, width)
    """
    (left, right), (top, bottom) = crop_size
    return frame[:, top: -bottom, left:-right]


def slice_by_time(xytp: np.ndarray, time_window: int):
    """
    Return indices where the events need to be sliced into equal time windows

    Args:
        xytp (np.ndarray):  Structured array of events
        time_window (int):  Length of time for each slice (ms)
    Returns:
        indices (np.ndarray): Indices to slices the events at
    """
    t = xytp["t"]
    time_points = np.arange(t[0] + time_window, t[-1], time_window)
    indices = np.searchsorted(t, time_points)
    return indices


def slice_by_count(xytp: np.ndarray, spike_count: int):
    """
    Return indices where the events need to be sliced into equal number of events specified by spike_count

    Args:
        xytp (np.ndarray):  Structured array of events
        spike_count (int):  Number of events per slice
    Returns:
        indices (np.ndarray): Indices to slices the events at
    """
    n_spk = len(xytp)
    # get rid of incomplete frames
    if len(xytp) % spike_count:
        indices = np.arange(spike_count, n_spk, spike_count)
    else:
        indices = np.arange(spike_count, n_spk + spike_count, spike_count)

    return indices


def accumulate_frames(list_xytp: List[np.ndarray], bins_y, bins_x) -> np.ndarray:
    """
    Convert xytp event lists to frames

    Args:
        list_xytp (List[np.ndarray]): A *list* of xytp, where each element in the list is a structured array of events
        bins_y (ListLike):  Bins to use for creating the frame
        bins_x (ListLike):  Bins to use for creating the frame

        Note: bins_y and bins_x are typically range(0, height_of_sensor) and range(0, width_of_sensor)
    Returns:
        raster: (np.ndaray): Numpy array with dimensions [N, polarity, height, width], where N is the length of list_xytp
    """
    frames = np.empty((len(list_xytp), 2, len(bins_y) - 1, len(bins_x) - 1), dtype=np.uint16)
    for i, slice_item in enumerate(list_xytp):
        frames[i] = np.histogramdd((slice_item["p"], slice_item["y"], slice_item["x"]),
                                   bins=((-1, 0.5, 2), bins_y, bins_x))[0]
    return frames


def identify_hot_pixels(xytp, shape: Tuple, hot_pixel_frequency: float):
    """
    Identify hot pixels with the given criterion

    Args:
        xytp (np.ndarray):  Structured array of events
        shape (Tuple): A tuple (height, width)
        hot_pixel_frequency (float): Threshold frequency for hot pixel in Hz

    Returns:
        hotpixels  : List of (x, y)

    """
    x, y = xytp["x"], xytp["y"]
    tottime = xytp["t"][-1] - xytp["t"][0]
    # xmin, ymin = 0, 0
    bins_x = np.arange(shape[1] + 1)
    bins_y = np.arange(shape[0] + 1)

    hist = np.histogram2d(x, y, bins=(bins_x, bins_y))[0]
    max_occur = hot_pixel_frequency * tottime * 1e-6
    hot_pixels = np.asarray((hist > max_occur).nonzero()).T
    return hot_pixels


def filter_hot_pixels(xytp, shape: Tuple, hot_pixel_frequency: float):
    """
    Filter hot pixels with the given criterion

    Args:
        xytp (np.ndarray):  Structured array of events
        shape (Tuple): A tuple (height, width)
        hot_pixel_frequency (float): Threshold frequency for hot pixel in Hz

    Returns:
        xytp_filtered (np.ndarray)  : Structured array of events

    """
    x, y = xytp["x"], xytp["y"]
    hot_pixels = identify_hot_pixels(xytp, shape, hot_pixel_frequency)

    mask = np.zeros(len(x), dtype=np.bool)
    for hp in hot_pixels:  # sigh (but 4x faster than np.unique)
        is_hot = np.logical_and(x == hp[0], y == hp[1])
        mask = np.logical_or(mask, is_hot)

    print(f"Found {len(hot_pixels)} hot pixels")
    print(f"Removed {mask.sum()} spikes from hot pixels")

    return xytp[~mask]


def create_raster_from_xytp(xytp: np.ndarray, dt: int, bins_y, bins_x):
    """
    Convert xytp events to a raster

    Args:
        xytp (np.ndarray):  Structured array of events
        dt (int):           Time window per slice in the raster
        bins_y (ListLike):  Bins to use for creating the frame
        bins_x (ListLike):  Bins to use for creating the frame

        Note: bins_y and bins_x are typically range(0, height_of_sensor) and range(0, width_of_sensor)
    Returns:
        raster: (np.ndaray): Numpy array with dimensions [time, polarity, height, width]
    """
    indices = slice_by_time(xytp, time_window=dt)
    sliced_xytp = np.split(xytp, indices)
    return accumulate_frames(sliced_xytp, bins_y, bins_x).astype(np.float32)
