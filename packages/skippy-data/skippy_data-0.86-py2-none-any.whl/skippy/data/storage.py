import logging
import os
import time
import numpy as np

from skippy.data.utils import get_file_name_urn

_LOCAL_SKIPPY_STORAGE = "/openfaas-local-storage/"


def has_local_storage_file(urn: str) -> bool:
    file_name = get_file_name_urn(urn)
    return os.path.exists(_LOCAL_SKIPPY_STORAGE + file_name)


def load_file_content_local_storage(urn: str):
    file_name = get_file_name_urn(urn)
    path = _LOCAL_SKIPPY_STORAGE + file_name
    logging.info('Reading file path %s' % path)
    start_time = time.time()
    content = np.load(path, allow_pickle=True)
    logging.info('File read in %s' % (time.time() - start_time))
    return content


def save_file_content_local_storage(content, urn: str):
    file_name = get_file_name_urn(urn)
    path = _LOCAL_SKIPPY_STORAGE + file_name
    logging.info('Save file in local storage %s' % path)
    start_time = time.time()
    try:
        np.save(path, content, allow_pickle=True)
        logging.info('File saved in %s' % (time.time() - start_time))
        return path
    except Exception as e:
        logging.error('Error trying to save file in local storage: %s', e)
