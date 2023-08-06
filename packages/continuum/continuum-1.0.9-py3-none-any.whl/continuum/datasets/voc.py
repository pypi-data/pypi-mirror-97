import os
from typing import Iterable, Set, Tuple, Union

import numpy as np

from continuum import download
from continuum.datasets.base import _ContinuumDataset


class PascalVOC2012(_ContinuumDataset):
    data_url = "http://pjreddie.com/media/files/VOCtrainval_11-May-2012.tar"
    segmentation_url = "http://cs.jhu.edu/~cxliu/data/SegmentationClassAug.zip"
    split_url = "http://cs.jhu.edu/~cxliu/data/list.zip"

    def __init__(self, data_path: str = "", download: bool = True) -> None:
        super().__init__(data_path, download)

    def _download(self):
        if not os.path.exists(os.path.join(self.data_path, "truc")):
            print("Downloading Pascal VOC dataset, it's slow!")
            download(self.data_url, self.data_path)
            # TODO untar

        if not os.path.exists(os.path.join(self.data_path, "SegmentationClassAug.zip")):
            path = download.download(self.segmentation_url, self.data_path)
            download.unzip(path)
        if not os.path.exists(os.path.join(self.data_path, "list.zip")):
            path = download.download(self.split_url, self.data_path)
            download.unzip(path)

    def init(self, train: bool) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        pass

    def parse_segmentation(self, train: bool) -> Tuple[np.ndarray, np.ndarray]:
        pass
