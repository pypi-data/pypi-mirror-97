import pytest
from pathlib import Path
import numpy as np
import cv2

from dvdp.utils.data import DataSaver, fetch_images


def test_create_and_load_chunks(tmpdir):
    data_saver = DataSaver(
        Path(tmpdir) / 'test',
        ['col1', 'col2'],
        chunk_size=4,
    )
    expected = {'col1': [], 'col2': []}
    for i in range(8):
        new = {'col1': i+1, 'col2': i}
        data_saver.add_data(new)
        expected['col1'].append(new['col1'])
        expected['col2'].append(new['col2'])

    result = DataSaver.load_data(Path(tmpdir) / 'test_000.gz')
    assert result == expected


def test_with_image(tmpdir):
    data_saver = DataSaver(
        Path(tmpdir) / 'test',
        ['col1', 'col2'],
        chunk_size=4,
    )
    expected = {'col1': [], 'col2': []}
    for i in range(8):
        image = np.full((4, 4), i)
        new = {'col1': image, 'col2': image}
        data_saver.add_data(new)
        expected['col1'].append(new['col1'])
        expected['col2'].append(new['col2'])

    result = DataSaver.load_data(Path(tmpdir) / 'test_000.gz')
    assert len(result) == len(expected)
    for images_rs, images_exp in zip(result.values(), expected.values()):
        assert len(images_rs) == len(images_exp)
        for image_rs, image_exp in zip(images_rs, images_exp):
            assert np.all(image_rs == image_exp)


def test_fetch_images(tmpdir):
    image_types = ['.jpg', '.bmp', '.tiff', '.png']
    exp_images = []
    i = 0
    for image_type in image_types:
        print(image_type)
        gray = np.full((10, 10), i*25, dtype=np.uint8)
        color = np.full((10, 10, 3), i*25, dtype=np.uint8)
        i += 1
        cv2.imwrite(str(tmpdir / f'{i}{image_type}'), gray)
        exp_images.append(gray)
        i += 1
        cv2.imwrite(str(tmpdir / f'{i}{image_type}'), color)
        exp_images.append(color)

    fetched_images = fetch_images(tmpdir, True)

    for fetched, expected in zip(fetched_images, exp_images):
        diff = fetched - expected
        assert np.all(diff == 0)
