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


def get_exif_dtm(file: Path):
    """Read EXIF DateTime field from `file`"""
    if file.suffix.lower() == '.mov':
        # MOV does not contains EXIF
        file = file.with_suffix('.thm')

    meta = pyexiv2.ImageMetadata(str(file))
    meta.read()
    try:
        return meta['Exif.Image.DateTime'].value
    except KeyError:
        return None


def get_target_name(file: Path) -> Path:
    """Builds a target file name to rename `file` to"""
    dtm: datetime = get_exif_dtm(file)

    target_name = MASK.format(dtm=(dtm and dtm.strftime(DTM_FMT)),
                              old_name=file.stem,
                              old_ext=file.suffix)

    print(f'"{file.name}"\t"{dtm}"\t"{file.with_name(target_name)}"')
    return target_name


def sequentially(files):
    for file_path in files:
        print_dtm(file_path)


def parallel(files):
    with ThreadPoolExecutor(8) as pool:
        _ = pool.map(print_dtm, files)


files = PATH.iterdir()
sequentially(files)
#parallel(files)