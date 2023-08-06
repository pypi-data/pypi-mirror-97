from .protocol import Protocol
from koturn.config import config


class Turn(Protocol):

  NAME = 'turn'

  def __init__(self):
    super(Turn, self).__init__(self.NAME)

  def format_ice_server_data(self, koturn_instance):
    return dict(
      urls=self.format_url(koturn_instance.ip, config.TURN_PORT),
      username=config.TURN_USERNAME,
      credential=config.TURN_PASSWORD,
    )
