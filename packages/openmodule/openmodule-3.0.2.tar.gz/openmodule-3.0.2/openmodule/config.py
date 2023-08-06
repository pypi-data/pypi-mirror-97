import logging
import os
import warnings
from socket import gethostname
from typing import Optional, Type, TypeVar

import builtins
import yaml
from pydantic import ValidationError
from pydantic.main import BaseModel


def _save_cast(obj, key, to_type, default):
    try:
        return to_type(obj[key])
    except (ValueError, TypeError, KeyError):
        return default


def int(key: str, default: int = 0) -> int:
    assert isinstance(default, (builtins.int,)), "default argument must be of type int"
    return _save_cast(os.environ, key, builtins.int, builtins.int(default))


def float(key: str, default: float = 0.0) -> float:
    assert isinstance(default, (builtins.int, builtins.float)), "default argument must be of type int or float"
    return _save_cast(os.environ, key, builtins.float, builtins.float(default))


def string(key: str, default: str = "") -> str:
    assert isinstance(default, str), "default argument must be of type string"
    res = os.environ.get(key, default)
    invalid_chars = "\"' \r\n\t"
    res = res.strip(invalid_chars)
    return res


def bool(key: str, default: bool = False) -> bool:
    assert isinstance(default, builtins.bool), "default argument must be of type bool"
    val = get(key) or ""
    val = val.upper().strip('\'" .,;-_')
    if not val:
        return default
    return val in ["T", "TRUE", "1", "Y", "YES", "J", "JA", "ON"]


def get(key: str, default: Optional[str] = "") -> str:
    return os.environ.get(key, default)


_inside_docker_cached = None


def _inside_docker():
    global _inside_docker_cached
    if _inside_docker_cached is not None:
        return _inside_docker_cached
    else:
        if os.path.exists('/.dockerenv'):
            _inside_docker_cached = True
            return _inside_docker_cached

        path = '/proc/self/cgroup'
        if os.path.isfile(path):
            with open(path, "r") as f:
                _inside_docker_cached = any('docker' in line for line in f)
        else:
            _inside_docker_cached = False

        return _inside_docker_cached


def debug():
    if "DEBUG" in os.environ:
        return bool("DEBUG", default=False)
    elif testing():
        return False
    else:
        return version() == "unknown" and not _inside_docker()


def log_level() -> int:
    log_levels = {
        "INFO": logging.INFO,
        "DEBUG": logging.DEBUG,
        "VERBOSE": logging.DEBUG,
        "WARN": logging.WARNING,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "ERR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
        "CRIT": logging.CRITICAL,
        "FATAL": logging.FATAL
    }
    default_log_level = logging.DEBUG if debug() else logging.INFO
    return log_levels.get(os.environ.get("LOG_LEVEL", "").upper(), default_log_level)


def version() -> str:
    version = string("VERSION", "")
    if not version:
        if os.path.isfile("VERSION"):
            with open("VERSION", "r") as f:
                version = f.read()
    if not version:
        version = "unknown"
    return version.strip("\r\n\t ")


def resource() -> str:
    resource = string("AUTH_RESOURCE", "")
    if not resource:
        resource = gethostname()
    return resource


def broker_pub(default: str = "tcp://127.0.0.1:10200") -> str:
    broker_host = string("BROKER_HOST", "")
    broker_pub_port = int("BROKER_PUB_PORT", 0)
    broker_pub = string("BROKER_PUB", "")

    if broker_pub:
        return broker_pub
    elif broker_host and broker_pub_port:
        # use legacy configs
        return "tcp://{}:{}".format(broker_host, broker_pub_port)
    else:
        return default


def broker_sub(default: str = "tcp://127.0.0.1:10100") -> str:
    broker_host = string("BROKER_HOST", "")
    broker_sub_port = int("BROKER_SUB_PORT", 0)
    broker_sub = string("BROKER_SUB", "")

    if broker_sub:
        return broker_sub
    elif broker_host and broker_sub_port:
        # use legacy configs
        return "tcp://{}:{}".format(broker_host, broker_sub_port)
    else:
        return default


def validate_config_module(config):
    required_keys = ["NAME", "RESOURCE", "VERSION", "DEBUG", "TESTING"]
    for x in required_keys:
        assert hasattr(config, x), f"the config module requires the variable {x}"

    if hasattr(config, "BROKER_PUB_PORT") or hasattr(config, "BROKER_SUB_PORT"):
        warnings.warn(
            "BROKER_(P/S)UB_PORT and BROKER_HOST are to be replaced with BROKER_(P/S)UB. In order to \n"
            "remain backwards compatible, you can use BROKER_PUB = config.broker_pub() which correctly \n"
            "interprets the deprecated environment variables",
            DeprecationWarning
        )


class SafeLoaderIgnoreUnknown(yaml.SafeLoader):
    def ignore_unknown(self, node):
        return None


SafeLoaderIgnoreUnknown.add_constructor(None, SafeLoaderIgnoreUnknown.ignore_unknown)

YamlType = TypeVar("YamlType", bound=BaseModel)


def yaml(model: Type[YamlType], path: str = None) -> YamlType:
    yaml_path = path or string("CONFIG_YAML", "")
    if not yaml_path:
        if debug():
            yaml_path = "../settings/default-debug.yml"
        elif testing():
            yaml_path = "../settings/default-testing.yml"
        else:
            yaml_path = "/data/config.yml"

    try:
        if os.path.exists(yaml_path):
            import yaml
            with open(yaml_path, "r") as f:
                a = yaml.load(f, SafeLoaderIgnoreUnknown)
                return model.parse_obj(a)
        else:
            return model()
    except ValidationError as e:
        logging.exception("error during config yaml loading, something is wrong with the configuration")
        raise e from None


def testing():
    return bool("TESTING", False)


def database_folder():
    path = string("DATABASE_FOLDER", f"../sqlite/")
    if testing():
        path += "test/"
    elif debug():
        path += "debug/"
    return path
