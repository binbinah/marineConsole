import yaml
import os


class MarineConfig:
    def __init__(self):
        super(MarineConfig, self).__init__()
        self.path = os.path.abspath(os.path.dirname(__file__))
        self.config = self.yml_config()

    def yml_config(self):
        """读取 config.yml 的配置。"""
        with open("/".join([self.path, "marine_config.yml"]), "r") as f:
            try:
                config = yaml.safe_load(f)
                return config
            except yaml.YAMLError as e:
                print("yml_config:{e}".format(e=e))
                return {}
