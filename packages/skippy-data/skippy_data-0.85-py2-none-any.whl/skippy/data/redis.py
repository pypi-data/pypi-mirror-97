import json
import logging
import os
from collections import defaultdict
from typing import List, Dict

import redis


def client():
    redis_host = os.environ.get('redis_host', None)
    logging.info('Redis host (%s)' % redis_host)
    rds = redis.Redis(decode_responses=True, host=redis_host)
    return rds


def get_dl_bandwidth(from_to: str, tar_to: str) -> float:
    bandwidth_json = client().hget(name='bandwidth_graph', key='bandwidth_graph')
    bandwidth = json.loads(bandwidth_json)
    return bandwidth[from_to].get(tar_to)


def get_storage_nodes(urn: str) -> List[str]:
    nodes_item_json = client().hget(name='nodes_item', key='nodes_item')
    nodes_item = json.loads(nodes_item_json)
    return nodes_item.get(urn)


def get_storage_bucket(bucket: str) -> List[str]:
    buckets_json = client().hget(name='buckets', key='buckets')
    nodes_item = json.loads(buckets_json)
    return nodes_item.get(bucket)


def get_files_size(path: str):
    items_size_json = client().hget(name='items_size', key='items_size')
    items_size = json.loads(items_size_json)
    return items_size.get(path)


def list_storage_pods_node(node: str) -> Dict[str, str]:
    logging.debug('list minio pods...')
    storage_pods_json = client().hget(name='storage_pods', key='storage_pods')
    storage_pods = json.loads(storage_pods_json)
    if storage_pods.get(node):
        return {k: v for k, v in storage_pods.items() if k == node}
    else:
        return storage_pods


def store_bandwidth(to_node: str, size: float, time: float):
    from_node = os.environ.get('node', None)
    data_bandwidth_graph = defaultdict(lambda: defaultdict())
    data_bandwidth_graph_json = client().hget(name='data_bandwidth_graph', key='data_bandwidth_graph')
    if data_bandwidth_graph_json is not None:
        data_bandwidth_graph.update(json.loads(data_bandwidth_graph_json))
    if from_node != to_node:
        data_bandwidth_graph[from_node][to_node] = round(size / time, 1)
        logging.info("data_bandwidth_graph %s", data_bandwidth_graph)
        client().hset(name='data_bandwidth_graph', key='data_bandwidth_graph', value=json.dumps(data_bandwidth_graph))

# def get_pod_node_name(pod_name: str) -> List[str]:
#    logging.debug('Get node for pod %s' % pod_name)
#    pods_node_json = client().hget(name='openfaas_pods', key='openfaas_pods')
#    pods_node_json = json.loads(pods_node_json)
#    return pods_node_json.get(pod_name)
