from pathlib import Path
from typing import Dict, List, Any, Union, Optional

import cv2
import numpy as np
import pandas as pd


class DataSaver:
    def __init__(self, name: Path, column_names: List[str], chunk_size=200):
        """
        Create a datasaver that saves data when chunksize has been reached.
        :param name: location and name of file chunk. e.g. /tmp/test will
        product /tmp/test_00x.gz chunks.
        :param column_names: column names to allow for records containing
        multiple values.
        :param chunk_size: chunk size in records that triggers a save.
        """
        self.__name = str(name)
        self.__chunk_size = chunk_size
        self.__identifiers = column_names
        self.__data_frame = None
        self.__reset()
        self.__chunk_idx = 0

    def __reset(self):
        self.__data_frame = pd.DataFrame({
            idn: [] for idn in self.__identifiers
        })

    def __save_maybe(self):
        if len(self.__data_frame) % self.__chunk_size != 0:
            return
        self.__save()

    def __save(self):
        chunk_filename = f'{self.__name}_{self.__chunk_idx:03d}.gz'
        print(f'Saving chunk {self.__chunk_idx} to {chunk_filename}...')
        self.__chunk_idx += 1
        self.__data_frame.to_pickle(chunk_filename, compression='gzip')
        print('Finished saving chunk file.')
        self.__reset()

    def add_data(self, data: Dict[str, List[Any]]):
        self.__data_frame = self.__data_frame.append(data, ignore_index=True)
        self.__save_maybe()

    @classmethod
    def load_data(cls, first_file):
        """Load data from chunks."""
        first_file = Path(first_file)
        dir = Path(first_file).parent
        ext = first_file.suffix

        if not first_file.exists():
            raise FileNotFoundError(f'Could not find first file {first_file}')

        file_idx = -1
        files = []
        while True:
            file_idx += 1
            file_name = str(first_file.stem).replace(
                '_000',
                f'_{file_idx:03}{ext}',
            )
            file_cur = dir / file_name
            if not file_cur.exists():
                break
            files.append(file_cur)

        data = pd.read_pickle(str(files[0]))
        for file in files[1:]:
            data = data.append(pd.read_pickle(str(file)))
        return {
            col: [x for x in data[col]]
            for col in data
        }

    def __del__(self):
        if len(self.__data_frame) != 0:
            self.__save()


def fetch_images(
    image_dir: Union[Path, str],
    as_np_array=False,
    glob: Optional[str]=None,
) -> List[Union[Path, np.ndarray]]:
    """
    Get all images from a directory.

    image_dir can also be a single file. It will raise a FileNotFoundError
    if image_dir does not exist.

    :param image_dir: Directory containing images or an image file location.
    :param as_np_array: It is possible to return the images as np.array's.
    :param glob: It is possible to return the images in dir using a glob
    seach pattern.
    :return: List of Paths to images or list of numpy arrays.
    """
    image_dir = Path(image_dir)
    if not image_dir.exists():
        raise FileNotFoundError(f'{image_dir} does not exist.')
    image_types = ['.jpg', '.bmp', '.tiff', '.png', '.gif']

    all_images = []
    if image_dir.is_file():
        all_images.append(image_dir)
    else:
        if glob is None:
            for image_type in image_types:
                all_images += [
                    image_loc
                    for image_loc in image_dir.glob('*' + image_type)
                ]
        else:
            all_images += [
                image_loc
                for image_loc in image_dir.glob(glob)
            ]
    all_images.sort()
    if as_np_array:
        return [
            cv2.imread(str(image_loc), cv2.IMREAD_UNCHANGED)
            for image_loc in all_images
        ]
