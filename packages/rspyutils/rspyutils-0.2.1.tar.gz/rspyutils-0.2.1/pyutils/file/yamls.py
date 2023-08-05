# !/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created on MAY 21, 2018
@author: zlh
"""
import yaml
from yaml import load, dump

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


def read_from_yaml(file: str) -> dict:
    with open(file) as f:
        # use safe_load instead load
        conf_dic = yaml.safe_load(f)
    return conf_dic


def get_config_str(file: str, key: str) -> str:
    conf_dic = read_from_yaml(file)
    return conf_dic.get(key, "")


def get_config_int(file: str, key: str) -> int:
    conf_dic = read_from_yaml(file)
    return conf_dic.get(key, 0)


def dump_into_yaml(file: str, dataMap: dict):
    with open(file, "w") as f:
        yaml.dump(dataMap, f)


def dump_into_yaml_str(file: str, document: str):
    dump_into_yaml(file, yaml.load(document))


if __name__ == "__main__":
    import pprint

    pprint.pprint(read_from_yaml("config.yaml"))
    import yaml

    document = """
      a: 1
      b:
        c: [3,5,6]
        d: 4
    """
    # print(yaml.dump(yaml.load(document), default_flow_style=True))
    dump_into_yaml("xx.yaml", yaml.load(document))
