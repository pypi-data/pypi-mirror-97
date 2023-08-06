import os
from koturn import env


class Config:
  ENV = ''

  def __init__(self):
    self.TURN_PORT = os.environ.get('TURN_PORT', 3478)
    self.TURN_USERNAME = os.environ.get('TURN_USERNAME')
    self.TURN_PASSWORD = os.environ.get('TURN_PASSWORD')

  def is_turn_configured(self):
    return self.TURN_USERNAME and self.TURN_PASSWORD


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