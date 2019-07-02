import datetime
import logging
import time
import pyexiv2
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(message)s')

PATH = Path(r'/run/media/dmitry/EOS_DIGITAL/DCIM/101CANON/')
DTM_FMT = '%Y%m%d-%H%M%S'
MASK = '{dtm}-{old_name}{old_ext}'


def get_meta(file: Path):
    """Extract `file` metadata"""
    if file.suffix.lower() == '.mov':
        # MOV does not contains EXIF
        file = file.with_suffix('.thm')

    meta = pyexiv2.ImageMetadata(str(file))
    meta.read()

    return meta


def get_exif_dtm(file: Path):
    """Read EXIF DateTime field from `file`"""
    meta = get_meta(file)

    try:
        return meta['Exif.Image.DateTime'].value
    except KeyError:
        return None


def get_target_path(file: Path) -> Path:
    """Builds a target file name to rename `file` to"""
    dtm: datetime = get_exif_dtm(file)

    target_name = MASK.format(dtm=(dtm and dtm.strftime(DTM_FMT)),
                              old_name=file.stem,
                              old_ext=file.suffix)
    target_path = file.with_name(target_name)
    return target_path


def sequentially(files):
    for file_path in files:
        target_path = get_target_path(file_path)
        print(f'"{file_path}" -> "{target_path}"')


def parallel(files):
    target_paths = []
    with ThreadPoolExecutor(8) as pool:
        target_paths = pool.map(lambda path: (path, get_target_path(path)), files)
    
    [print(f'"{file_path}" -> "{target_path}"') for file_path, target_path in target_paths]


files = PATH.iterdir()
sequentially(files)
#parallel(files)