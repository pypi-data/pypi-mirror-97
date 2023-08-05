from aermanager.aerparser import load_events_from_file
from aermanager import preprocess
import numpy as np
from pathlib import Path

TEST_FILE = Path(__file__).parent / "data" / "class2" / "data_sample.aedat4"


def test_slice_by_time():
    shape, xytp = load_events_from_file(TEST_FILE)
    assert(shape == (240, 320))
    time_window = 10000
    indices = preprocess.slice_by_time(xytp, time_window)  # 10ms
    sliced_xytp = np.split(xytp, indices)[:-1]
    for slice in sliced_xytp:
        tw_actual = slice["t"][-1] - slice["t"][0]
        assert(tw_actual <= time_window)


def test_slice_by_count_in_exact():
    shape, xytp = load_events_from_file(TEST_FILE)
    assert(shape == (240, 320))
    spk_count = 1000
    indices = preprocess.slice_by_count(xytp, spk_count)
    sliced_xytp = np.split(xytp, indices)[:-1]
    for i, slice in enumerate(sliced_xytp):
        count_actual = len(slice)
        assert(count_actual == spk_count)

    assert(len(xytp) - sum([len(slice) for slice in sliced_xytp]) < spk_count)


def test_slice_by_count_exact():
    shape, xytp = load_events_from_file(TEST_FILE)
    spk_count = 1000
    xytp = xytp[:spk_count * int(len(xytp) / spk_count)]
    assert(shape == (240, 320))
    indices = preprocess.slice_by_count(xytp, spk_count)
    sliced_xytp = np.split(xytp, indices)[:-1]
    for i, slice in enumerate(sliced_xytp):
        count_actual = len(slice)
        assert(count_actual == spk_count)

    assert(len(xytp) - sum([len(slice) for slice in sliced_xytp]) < spk_count)


def test_accumulate_frames_spike_count():
    shape, xytp = load_events_from_file(TEST_FILE)
    spk_count = 1000
    indices = preprocess.slice_by_count(xytp, spk_count)
    sliced_xytp = np.split(xytp, indices)[:-1]
    frames = preprocess.accumulate_frames(
        sliced_xytp, np.arange(shape[0] + 1), np.arange(shape[1] + 1))
    for f in frames:
        assert(f.shape == (2, *shape))
        assert (f.sum() == spk_count)


def test_accumulate_frames_time_window():
    shape, xytp = load_events_from_file(TEST_FILE)
    time_window = 50000
    indices = preprocess.slice_by_time(xytp, time_window)[:-1]
    sliced_xytp = np.split(xytp, indices)[:-1]
    frames = preprocess.accumulate_frames(
        sliced_xytp, np.arange(shape[0] + 1), np.arange(shape[1] + 1))
    for i, f in enumerate(frames):
        assert(f.shape == (2, *shape))
        assert (f.sum() == len(sliced_xytp[i]))


def test_crop_events_obvious():
    shape, xytp = load_events_from_file(TEST_FILE)
    cropped_xytp, new_shape = preprocess.crop_events(xytp, input_shape=shape,
                                                     crop_size=((0, 0), (0, 0)))
    assert(len(cropped_xytp) == len(xytp))
    assert(new_shape == shape)


def test_crop_events():
    shape, xytp = load_events_from_file(TEST_FILE)
    print(shape)
    cropped_xytp, new_shape = preprocess.crop_events(xytp, input_shape=shape,
                                                     crop_size=((10, 50), (5, 7)))
    assert(len(cropped_xytp) != len(xytp))
    # Check width
    assert(cropped_xytp["x"].max() == shape[1] - 50 - 10 - 1)
    assert(cropped_xytp["x"].min() == 0)
    # Check height
    assert(cropped_xytp["y"].max() == shape[0] - 5 - 7 - 1)
    assert(cropped_xytp["y"].min() == 0)

    assert new_shape == ((shape[0] - 5 - 7), (shape[1] - 50 - 10))


def test_crop_frame():
    shape, xytp = load_events_from_file(TEST_FILE)
    spk_count = 1000
    indices = preprocess.slice_by_count(xytp, spk_count)
    sliced_xytp = np.split(xytp, indices)[:-1]
    frames = preprocess.accumulate_frames(
        sliced_xytp, np.arange(shape[0] + 1), np.arange(shape[1] + 1))
    for f in frames:
        frame_cropped = preprocess.crop_frame(f, crop_size=((10, 50), (5, 7)))
        assert(frame_cropped.shape == (2, shape[0] - 5 - 7, shape[1] - 10 - 50))


def test_filter_hot_pixels():
    shape, xytp = load_events_from_file(TEST_FILE)
    xytp_filtered = preprocess.filter_hot_pixels(xytp, shape=shape, hot_pixel_frequency=1000)
    assert(len(xytp_filtered) <= len(xytp))
