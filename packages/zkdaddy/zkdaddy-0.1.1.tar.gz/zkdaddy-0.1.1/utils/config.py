import sys
import json
from os.path import expanduser
from pathlib import Path
from pydantic import BaseModel
from colorama import Fore


class Config(BaseModel):
    node_path_pre: str
    zk_address: dict


def build_config():
    home_path_str = expanduser("~")
    config_path = Path(f"{home_path_str}/.config/.zkdaddy")
    if not config_path.exists():
        print(Fore.RED + f"not have config file, please create config file in {config_path}")
        sys.exit(0)
    config_body = config_path.read_text(encoding="utf-8")
    # print(config_body)
    config_data = json.loads(config_body)
    c = Config(**config_data)
    return c


config = build_config()
