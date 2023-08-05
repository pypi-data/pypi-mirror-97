import logging
import os
import time
from collections import defaultdict
from typing import io
import numpy as np

from minio import Minio
from minio.error import ResponseError

from skippy.data import utils
from skippy.data.priorities import get_best_node
from skippy.data.redis import list_storage_pods_node, store_bandwidth
from skippy.data.storage import has_local_storage_file, save_file_content_local_storage, load_file_content_local_storage
from skippy.data.utils import get_bucket_urn, get_file_name_urn

_CONSUME_LABEL = 'data.consume'
__PRODUCE_LABEL = 'data.produce'


def has_pod_file(urn: str, minio_addr: str) -> bool:
    try:
        if has_pod_bucket(get_bucket_urn(urn), minio_addr):
            stat = minio_client(minio_addr).stat_object(get_bucket_urn(urn), get_file_name_urn(urn))
            return stat.size > 0
        else:
            return False
    except ResponseError as err:
        logging.warning('MinioClientException: %s', err.message)
        return False


def has_pod_bucket(bucket: str, minio_addr: str) -> bool:
    try:
        return minio_client(minio_addr).bucket_exists(bucket)
    except ResponseError as err:
        logging.error('MinioClientException: %s', err.message)
        return False


def minio_client(minio_addr: str) -> Minio:
    minio_ac = os.environ.get('MINIO_AC', None)
    minio_sc = os.environ.get('MINIO_SC', None)
    client = Minio(minio_addr,
                   access_key=minio_ac,
                   secret_key=minio_sc,
                   secure=False)
    return client


def download_files(urns: str):
    logging.info('download files from urn(s)  %s' % urns)
    data_artifact = defaultdict(list)
    urn_paths = utils.get_urn_from_path(_CONSUME_LABEL, urns)
    for urn in urn_paths:
        data_file = download_file(urn)
        if data_file is not None:
            data_artifact[urn].append(data_file)
    return data_artifact


def download_file(urn: str) -> str:
    logging.info('download file from urn  %s' % urn)
    # what is the best pod
    # where do we make this decisison
    # find the best pod to download
    if has_local_storage_file(urn):
        logging.info('file loaded from temp storage %s' % urn)
        return load_file_content_local_storage(urn)
    else:
        best_storage = get_best_node(urn)
        minio_addrs = list_storage_pods_node(best_storage)
        for node, minio_addr in minio_addrs.items():
            if has_pod_file(urn, minio_addr):
                client = minio_client(minio_addr)
                start = time.perf_counter()
                response = client.get_object(get_bucket_urn(urn), get_file_name_urn(urn))
                content = str(response.read().decode('utf-8'))
                end = time.perf_counter()
                size = int(response.headers.get('content-length', '0'))
                logging.debug('file download from %s in %s' % (node, (end - start)))
                store_bandwidth(node, size, end - start)
                return content


def upload_file(content, urn: str) -> None:
    logging.info('upload urn %s' % urn)
    if urn is None:
        urn = utils.get_urn_from_path(__PRODUCE_LABEL, urn)[0]
    save_file_content_local_storage(content, urn)
    best_none = get_best_node(urn)
    file_name = get_file_name_urn(urn)
    try:
        minio_addrs = list_storage_pods_node(best_none)
        for node, minio_addr in minio_addrs.items():
            if has_pod_bucket(get_bucket_urn(urn), minio_addr):
                client = minio_client(minio_addr)
                start = time.perf_counter()
                buf = np.array(content, dtype="object").tobytes()
                size = len(buf)
                client.put_object(get_bucket_urn(urn), file_name, io.BytesIO(buf), size,
                                  content_type='application/json')

                end = time.perf_counter()
                logging.debug('file upload size %s from %s in %s' % (node, size, (end - start)))
                store_bandwidth(node, size, end - start)
                return
    except ResponseError as e:
        logging.error('MinioClientException: %s', e.message)
