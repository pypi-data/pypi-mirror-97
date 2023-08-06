import sys
import json
from kazoo.client import KazooClient
from utils.printx import print_json
from utils.config import config
from colorama import Fore


def conf_path_by_service_name(service_name):
    return f"{config.node_path_pre}/{service_name}"


def create_zk(zk_client, path, content):
    content = json.dumps(content).encode()
    zk_client.create(path, content, makepath=True)


def new_zk_client(zk_address):
    zk_client = KazooClient(zk_address)
    zk_client.start()
    return zk_client


def load_config(zk_client, conf_path):
    return json.loads(zk_client.get(conf_path)[0].decode())


def update_zk_config(zk_client, config_path, data):
    zk_config = json.loads(zk_client.get(config_path)[0].decode())
    zk_config.update(data)
    zk_client.set(config_path, json.dumps(zk_config).encode())


def show_zk_config(service_name, stage):
    conf_path = conf_path_by_service_name(service_name)
    zk_client = new_zk_client(config.zk_address[stage])
    res = load_config(zk_client, conf_path)
    print_json(res)


def set_zk_key(service_name, stage, key, value_type, value):
    conf_path = conf_path_by_service_name(service_name)
    zk_client = new_zk_client(config.zk_address[stage])
    res = load_config(zk_client, conf_path)
    if value_type == "str":
        res[key] = str(value)
    elif value_type == "int":
        res[key] = int(value)
    elif value_type == "json":
        res[key] = json.loads(value)
    else:
        print(Fore.RED + f"cannot find value type {value_type}")
        sys.exit(1)
    update_zk_config(zk_client, conf_path, res)


def del_zk_key(service_name, stage, key):
    conf_path = conf_path_by_service_name(service_name)
    zk_client = new_zk_client(config.zk_address[stage])
    res = load_config(zk_client, conf_path)
    if key in res:
        del res[key]
        update_zk_config(zk_client, conf_path, res)
