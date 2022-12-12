from pathlib import Path

import yaml
from yaml import CLoader as Loader

from etmfa_core.aidoc.io import read_iqv_xml

LOCAL_CONFIG_PATH = Path(__file__).parent.parent.joinpath("server_config.yaml")
GLOBAL_CONFIG_PATH = Path(__file__).parent.parent.joinpath("config.xml")

localConfig = {'debug': True}
globalConfig = None


def load(environment, configs=(LOCAL_CONFIG_PATH, GLOBAL_CONFIG_PATH)):
    loadLocalConfig(environment, configs[0])
    loadGlobalConfig(configs[1])


def loadLocalConfig(environment, config):
    global localConfig

    if isinstance(config, str):
        config = Path(config)
    if not config.exists():
        raise RuntimeError("File does not exists:", config)

    with config.open() as f:
        conf = yaml.load(f, Loader=Loader)
        localConfig = conf[environment]


def loadGlobalConfig(config):
    global globalConfig

    if isinstance(config, str):
        config = Path(config)
    if not config.exists():
        raise RuntimeError("File does not exists:", config)

    globalConfig = read_iqv_xml(str(config))
