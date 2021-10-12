import os

from simple_storage.libs.singleton import MetaSingleton
from configloader import ConfigLoader

config_abs_path = "/".join(os.path.abspath(__file__).split('/')[0:-2])

ENV_PREFIX = "simple_storage"


class Config(metaclass=MetaSingleton):
    def __init__(self, config_file_path=os.path.join(config_abs_path, 'config.yml')):
        self.config_loader = ConfigLoader()
        env_config_path = os.getenv(f"{ENV_PREFIX}_CONFIG")
        if env_config_path:
            config_file_path = env_config_path
        self.config_loader.update_from_yaml_file(config_file_path)
        self.config_loader.update_from_env_namespace(ENV_PREFIX)

    def get(self, setting_name):
        return self.config_loader.get(setting_name, None)

    def to_dict(self):
        loader = self.config_loader
        return {key: loader.get(key) for key in loader.keys()}


LOGGING_LEVEL = "LOGGING_LEVEL"
LOGGING_FORMAT = "LOGGING_FORMAT"
DB_PATH = "DB_PATH"
USE_ENCRYPTION = "USE_ENCRYPTION"
MASTER_KEY = "MASTER_KEY"
USE_AUTH = "USE_AUTH"
ENCRYPTION_KEY = "ENCRYPTION_KEY"
PRECONFIGURED_ACCESS_TOKENS = "PRECONFIGURED_ACCESS_TOKENS"
