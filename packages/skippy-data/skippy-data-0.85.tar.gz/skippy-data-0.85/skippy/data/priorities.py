import logging
import os

from skippy.data.redis import get_files_size, get_storage_nodes, get_dl_bandwidth, get_storage_bucket
from skippy.data.utils import get_bucket_urn



def get_best_node(urn: str):
    node_name = os.environ.get('node', None)
    logging.debug("Node %s" % node_name)

    file_size = get_files_size(urn)
    if file_size is None:
        return None

    time = 0
    max_bw_storage = None

    storage_nodes = get_storage_nodes(urn)
    if storage_nodes is None:
        storage_nodes = get_storage_bucket(get_bucket_urn(urn))
    # find the storage node that holds the data and has the minimal bandwidth in the required direction (down)
    max_bw = 0
    logging.debug('Calculations node [%s] to storage options %s to transfer %s' % (node_name, storage_nodes, urn))
    for storage in storage_nodes:
        logging.debug('Node [%s] to storage [%s]' % (node_name, storage))
        if storage == node_name:
            logging.debug('Node and storage the same. Time = 0')
            return storage

        bandwidth = get_dl_bandwidth(storage, node_name)
        if bandwidth is not None and bandwidth > max_bw:
            max_bw = bandwidth
            max_bw_storage = storage

    if max_bw_storage and file_size:
        time += int(file_size / max_bw)
    logging.debug('[%s] is the best storage from node [%s] to transfer %s. Time = %s' % (
        max_bw_storage, node_name, urn, time))
    return max_bw_storage
