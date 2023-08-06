import json


def print_json(d):
    dd = json.dumps(d, sort_keys=True, indent=4, separators=(', ', ': '), ensure_ascii=False)
    print(dd)
