import numpy as np


def test_float():
    from aermanager.transform import apply_by_channel
    from torchvision.transforms import RandomAffine
    tr = RandomAffine(0.)
    tr = apply_by_channel(tr)

    img = np.random.random((2, 10, 20)).astype(np.float32) - 0.5
    res = tr(img)

    assert np.all(img == res)
    assert img.dtype == res.dtype


def test_uint8():
    from aermanager.transform import apply_by_channel
    from torchvision.transforms import RandomAffine
    tr = RandomAffine(0.)
    tr = apply_by_channel(tr)

    img = np.random.choice(256, size=(2, 10, 20)).astype(np.uint8)
    res = tr(img)

    assert np.all(img == res)
    assert img.dtype == res.dtype


def test_identity_trasform():
    from aermanager.transform import apply_by_channel
    from torchvision.transforms import RandomAffine, ToPILImage
    tr = RandomAffine((10, 10), scale=(0.8, 0.8))
    img = np.random.choice(256, size=(1, 10, 20)).astype(np.uint8)

    res = tr(ToPILImage()(img[0]))
    tr = apply_by_channel(tr)
    res2 = tr(img)[0]

    assert np.all(res2 == res)


def test_transform_consistency():
    # this is useful to check that all channels are transformed equally
    # even if the transformation is not deterministic: important
    from aermanager.transform import apply_by_channel
    from torchvision.transforms import RandomAffine
    tr = RandomAffine(10, scale=(1.1, 1.3))
    img = np.random.choice(256, size=(1, 10, 20)).astype(np.uint8)
    img = np.repeat(img, axis=0, repeats=2)

    # check that the test is correct to start with
    assert np.all(img[0] == img[1])
    assert np.shape(img) == (2, 10, 20)

    tr = apply_by_channel(tr)
    res = tr(img)

    # check that the transformation has acted equally on the inputs
    assert np.all(res[0] == res[1])
    # check that the transformation has actually done something
    assert not np.all(res[0] == img[0])


def test_transform_consistency_4d():
    # this is useful to check that all channels are transformed equally
    # even if the transformation is not deterministic: important
    from aermanager.transform import apply_by_channel
    from torchvision.transforms import RandomAffine
    tr = RandomAffine(10, scale=(1.1, 1.3))
    img = np.random.choice(256, size=(1, 1, 10, 20)).astype(np.uint8)
    img = np.repeat(img, axis=0, repeats=2)
    img = np.repeat(img, axis=1, repeats=2)

    # check that the test is correct to start with
    assert np.all(img[0, 0] == img[1, 1])
    assert np.shape(img) == (2, 2, 10, 20)

    tr = apply_by_channel(tr)
    res = tr(img)

    # check that the transformation has acted equally on the inputs
    assert np.all(res[0, 0] == res[1, 1])
    # check that the transformation has actually done something
    assert not np.all(res[0, 0] == img[0, 0])


def test_transform_randomness():
    # the transform should be consistent on a single image, BUT should
    # change when we use multiple images, calling transform multiple times
    from aermanager.transform import apply_by_channel
    from torchvision.transforms import RandomAffine
    tr = RandomAffine(10, scale=(1.1, 1.3))
    img = np.random.choice(256, size=(1, 10, 20)).astype(np.uint8)
    img2 = img.copy()

    # check that the test is correct to start with
    assert np.all(img == img2)

    tr = apply_by_channel(tr)
    res = tr(img)
    res2 = tr(img2)

    # check that the transformation has acted equally on the inputs
    assert not np.all(res == res2)
    # check that the transformation has actually done something
    assert not np.all(res == img)
