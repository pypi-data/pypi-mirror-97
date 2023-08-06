import yaml

_CONFIG_FILE: str = 'function/skippy.yml'


def get_multiple_urns(urns: str) -> list:
    return list(urns.split(","))


def get_bucket_urn(urn: str) -> str:
    data = urn.split("/", 2)
    return data[0]


def get_file_name_urn(urn: str) -> str:
    data = urn.split("/", 2)
    return data[1]


def get_urn_from_path(label_suffix: str, urns: str = None):
    if urns is not None and '/' in urns:
        return get_multiple_urns(urns)
    else:
        return get_urn_from_config_file(label_suffix)


def get_urn_from_config_file(label_suffix: str):
    data = parse_yaml(_CONFIG_FILE)
    label_arr = label_suffix.split('.')
    value = data[label_arr[0]][label_arr[1]]
    return [v.replace('.', '/', 1) for v in value]


def parse_yaml(config_file: str = None):
    if not config_file:
        config_file = _CONFIG_FILE
    with open(config_file) as f:
        return yaml.safe_load(f)

