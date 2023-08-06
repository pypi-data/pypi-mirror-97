import os
from jolly import env


class Config:
  ENV = ''

  def __init__(self):
    self.BALANCED_MAX_INSTANCE_LOAD = os.environ.get('BALANCED_MAX_INSTANCE_LOAD', 100)


class ProdConfig(Config):
  ENV = env.PROD


class StagingConfig(Config):
  ENV = env.STAGING


class DevConfig(Config):
  ENV = env.DEV


def get_config():
  config_class = globals().get('{}Config'.format(env.env().capitalize()))
  return config_class() if config_class else None


config = get_config()